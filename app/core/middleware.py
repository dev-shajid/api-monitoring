import time
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from prometheus_client import Counter, Histogram, Gauge

# Get logger
logger = logging.getLogger("api")

# Prometheus Metrics
REQUESTS = Counter("api_requests_total", "Total count of requests", ["method", "endpoint"])
EXCEPTIONS = Counter("api_exceptions_total", "Total count of exceptions", ["endpoint", "exception_type"])
LATENCY = Histogram("api_request_duration_seconds", "Request duration", ["method", "endpoint"])
ACTIVE_REQUESTS = Gauge("api_active_requests", "Number of currently active requests")

def setup_middleware(app: FastAPI):
    """Configure all middleware for the application"""
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Request metrics middleware
    @app.middleware("http")
    async def metrics_middleware(request: Request, call_next):
        method = request.method
        endpoint = request.url.path
        REQUESTS.labels(method=method, endpoint=endpoint).inc()
        ACTIVE_REQUESTS.inc()

        start_time = time.time()
        client_ip = request.client.host if request.client else "unknown"
        logger.info(f"➡️ {method} {endpoint} from {client_ip}")

        try:
            response = await call_next(request)
            duration = time.time() - start_time
            
            # Add structured field for status_code to be extracted by Loki
            extra = {"status_code": response.status_code}
                
            response.headers["X-Process-Time"] = str(duration)
            return response
        except Exception as e:
            exception_type = type(e).__name__
            # For exceptions, add status code 500 as a structured field
            extra = {"status_code": 500}
            EXCEPTIONS.labels(endpoint=endpoint, exception_type=exception_type).inc()
            logger.error(f"500 - ❌ Exception on {method} {endpoint}: {e}", extra=extra)
            raise e
        finally:
            LATENCY.labels(method=method, endpoint=endpoint).observe(time.time() - start_time)
            ACTIVE_REQUESTS.dec()
    
    # Custom exception handlers
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Custom handler for HTTP exceptions like 404 Not Found"""
        status_code = exc.status_code
        detail = str(exc.detail)
        
        # Log the error
        logger.error(
            f"{status_code} - 🚫 HTTP - {request.method} {request.url.path}: {detail}", 
            extra={"status_code": status_code}
        )
        
        return JSONResponse(
            status_code=status_code,
            content={"detail": detail},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Custom handler for request validation errors"""
        error_messages = [f"{err['loc']}: {err['msg']}" for err in exc.errors()]
        detail = "; ".join(error_messages)
        
        # Log the validation error
        logger.error(
            f"422 - ⚠️ Validation Error - {request.method} {request.url.path}: {detail}", 
            extra={"status_code": 422}
        )
        
        return JSONResponse(
            status_code=422,
            content={"detail": error_messages},
        )