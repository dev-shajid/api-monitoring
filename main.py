import random
import time
import logging
import socket
import os
import sys
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
import uvicorn
import psutil
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

# Custom handler that silently fails if logging to Loki fails
class SafeHandler(logging.Handler):
    def __init__(self, target_handler):
        super().__init__()
        self.target_handler = target_handler
        
    def emit(self, record):
        try:
            self.target_handler.emit(record)
        except Exception:
            # Silently fail - explicitly suppress the handleError call
            pass

    def handleError(self, record):
        # Override handleError to prevent any error output
        pass

# Setup basic logging first - file and console only
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.FileHandler("logs/api.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("api-monitoring")

# Quietly try setting up Loki handler - without any prints or warnings
loki_available = False
try:
    import logging_loki
    # Using host.docker.internal instead of localhost to properly reach Loki container from host machine
    loki_url = "http://localhost:3100/loki/api/v1/push"
    
    logger.info(f"Attempting to connect to Loki at {loki_url}")
    
    loki_direct_handler = logging_loki.LokiHandler(
        url=loki_url, 
        tags={"service": "api-server", "host": socket.gethostname()},
        version="1",
        # Removed timeout and retries parameters as they're not supported
    )
    # Wrap the Loki handler in our SafeHandler to prevent exceptions
    loki_handler = SafeHandler(loki_direct_handler)
    logger.addHandler(loki_handler)
    loki_available = True
    logger.info("Successfully connected to Loki logging service")
except Exception as e:
    # Log the exception but continue without Loki
    logger.warning(f"Failed to connect to Loki: {str(e)}")
    pass

# Log startup info
logger.info(f"Initializing application on {socket.gethostname()}")
logger.info(f"Python version: {sys.version}")
logger.info(f"Current time: {datetime.now().isoformat()}")

# FastAPI App Setup with modern lifespan pattern
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    logger.info("🚀 Application startup complete")
    yield
    # Shutdown code
    logger.info("🛑 Application shutdown initiated")

app = FastAPI(
    title="API Monitoring Demo",
    description="FastAPI application with Prometheus and Loki integration",
    version="0.1.0",
    lifespan=lifespan
)

# Prometheus Metrics
REQUESTS = Counter("api_requests_total", "Total count of requests", ["method", "endpoint"])
EXCEPTIONS = Counter("api_exceptions_total", "Total count of exceptions", ["endpoint", "exception_type"])
LATENCY = Histogram("api_request_duration_seconds", "Request duration", ["method", "endpoint"])
ACTIVE_REQUESTS = Gauge("api_active_requests", "Number of currently active requests")
COIN_FLIPS = Counter("coin_flips_total", "Total number of coin flips")
HEADS_COUNT = Counter("heads_total", "Total number of heads outcomes")

CPU_PERCENT = Gauge("system_cpu_percent", "CPU usage percentage")
MEM_PERCENT = Gauge("system_memory_percent", "Memory usage percentage")
DISK_PERCENT = Gauge("system_disk_percent", "Disk usage percentage", ["mount"])
NETWORK_SENT = Gauge("system_network_bytes_sent", "Network bytes sent", ["interface"])
NETWORK_RECV = Gauge("system_network_bytes_received", "Network bytes received", ["interface"])


# Middleware: CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Model
class CoinFlipResponse(BaseModel):
    heads: int
    tails: int
    ratio: float
    duration_ms: float
    
    
    
# Update metrics periodically
@app.on_event("startup")
async def start_metrics_collection():
    def collect_metrics():
        while True:
            # CPU
            CPU_PERCENT.set(psutil.cpu_percent())
            
            # Memory
            MEM_PERCENT.set(psutil.virtual_memory().percent)
            
            # Disk
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    DISK_PERCENT.labels(mount=partition.mountpoint).set(usage.percent)
                except:
                    pass
                    
            # Network
            net_io = psutil.net_io_counters(pernic=True)
            for interface, counters in net_io.items():
                NETWORK_SENT.labels(interface=interface).set(counters.bytes_sent)
                NETWORK_RECV.labels(interface=interface).set(counters.bytes_recv)
                
            time.sleep(5)  # Collect every 5 seconds
    
    # Run in a separate thread
    import threading
    thread = threading.Thread(target=collect_metrics, daemon=True)
    thread.start()

# Request Monitoring Middleware
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

# Add custom exception handler for 404 Not Found errors
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

# Endpoints

@app.get("/", tags=["Base"])
def root():
    logger.info("🏠 Root endpoint hit")
    return {"message": "API Monitoring with Prometheus and Loki"}

@app.get("/metrics", response_class=PlainTextResponse)
async def metrics():
    return PlainTextResponse(generate_latest().decode(), media_type=CONTENT_TYPE_LATEST)

@app.get("/flip-coins", response_model=CoinFlipResponse, tags=["Demo"])
def flip_coins(times: int = 10):
    if times <= 0:
        raise HTTPException(status_code=400, detail="Times must be > 0")
    if times > 1000:
        logger.warning(f"⚠️ Large coin flip request: {times}")
    
    COIN_FLIPS.inc(times)
    logger.info(f"🎲 Flipping {times} coins")

    start = time.time()
    heads = sum(random.choice([0, 1]) for _ in range(times))
    tails = times - heads
    duration = time.time() - start
    HEADS_COUNT.inc(heads)

    if heads == tails:
        logger.warning("🪙 Perfect balance! Suspicious...")
    elif heads == times:
        logger.warning("🪙 All heads!")
    elif heads == 0:
        logger.warning("🪙 All tails!")

    return {
        "heads": heads,
        "tails": tails,
        "ratio": heads / times,
        "duration_ms": duration * 1000
    }

@app.get("/error", tags=["Debug"])
def throw_error():
    error_type = random.choice(["value", "key", "type", "runtime"])
    # Using 500 as the status code since these are server errors
    logger.error(f"500 - 🔴 Triggered {error_type} error", extra={"status_code": 500})
    if error_type == "value":
        raise ValueError("Boom! ValueError triggered.")
    elif error_type == "key":
        raise KeyError("Oops! KeyError triggered.")
    elif error_type == "type":
        raise TypeError("Bruh! TypeError triggered.")
    else:
        raise RuntimeError("Chaos! RuntimeError triggered.")

@app.get("/health", tags=["Monitoring"])
def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "hostname": socket.gethostname()
    }

@app.get("/log-levels", tags=["Debug"])
def log_levels():
    logger.debug("Debug level log")
    logger.info("Info level log")
    logger.warning("Warning level log")
    logger.error("500 - Error level log", extra={"status_code": 500})
    logger.critical("Critical level log")
    return {"message": "Logged at all levels"}

@app.get("/loki-status", tags=["Monitoring"])
def loki_status():
    """Check if Loki logging is operational"""
    # Get the real URL that was used for Loki configuration
    loki_url = "http://host.docker.internal:3100/loki/api/v1/push" if sys.platform in ["darwin", "win32"] else "http://localhost:3100/loki/api/v1/push"
    return {
        "loki_enabled": loki_available,
        "loki_url": loki_url if loki_available else None,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    logger.info("🔥 Launching FastAPI app...")
    uvicorn.run(app, host="0.0.0.0", port=8000)