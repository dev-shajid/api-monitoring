import time
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from prometheus_client import Counter, Histogram, Gauge
from opentelemetry import trace
from opentelemetry.trace.status import Status, StatusCode

# Get logger
logger = logging.getLogger("api")
tracer = trace.get_tracer(__name__)

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
    
    # Request metrics and tracing middleware
    @app.middleware("http")
    async def metrics_and_tracing_middleware(request: Request, call_next):
        method = request.method
        endpoint = request.url.path
        
        # Skip tracing for excluded endpoints
        if endpoint != "/metrics":
            with tracer.start_as_current_span(
                name=f"{method} {endpoint}",
                kind=trace.SpanKind.SERVER,
            ) as span:
                try:
                    # Add request details to span
                    span.set_attribute("http.method", method)
                    span.set_attribute("http.url", str(request.url))
                    span.set_attribute("http.route", endpoint)
                    
                    # Add custom attributes if needed
                    client_ip = request.client.host if request.client else "unknown"
                    span.set_attribute("client.ip", client_ip)
                    
                    # Standard metrics
                    REQUESTS.labels(method=method, endpoint=endpoint).inc()
                    ACTIVE_REQUESTS.inc()
                    start_time = time.time()

                    # Execute the request
                    response = await call_next(request)
                    
                    # Add response information to span
                    span.set_attribute("http.status_code", response.status_code)
                    duration = time.time() - start_time
                    span.set_attribute("duration_ms", duration * 1000)
                    
                    # Update metrics
                    LATENCY.labels(method=method, endpoint=endpoint).observe(duration)
                    
                    return response
                    
                except Exception as e:
                    # Handle exceptions
                    exception_type = type(e).__name__
                    EXCEPTIONS.labels(endpoint=endpoint, exception_type=exception_type).inc()
                    
                    # Add error details to span
                    span.set_status(Status(StatusCode.ERROR))
                    span.record_exception(e)
                    span.set_attribute("error.type", exception_type)
                    span.set_attribute("error.message", str(e))
                    
                    logger.error(f"500 - ❌ Exception on {method} {endpoint}: {e}")
                    raise
                finally:
                    ACTIVE_REQUESTS.dec()
        else:
            # For excluded endpoints, just process without tracing
            return await call_next(request)

    # Update the exception handlers to include tracing
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Custom handler for HTTP exceptions"""
        current_span = trace.get_current_span()
        if current_span:
            current_span.set_attribute("error.type", "HTTPException")
            current_span.set_attribute("error.status_code", exc.status_code)
            current_span.set_attribute("error.detail", str(exc.detail))
            current_span.set_status(Status(StatusCode.ERROR))

        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Custom handler for validation errors"""
        current_span = trace.get_current_span()
        if current_span:
            error_messages = [f"{err['loc']}: {err['msg']}" for err in exc.errors()]
            current_span.set_attribute("error.type", "ValidationError")
            current_span.set_attribute("error.detail", "; ".join(error_messages))
            current_span.set_status(Status(StatusCode.ERROR))

        return JSONResponse(
            status_code=422,
            content={"detail": [err for err in exc.errors()]},
        )