import os
import sys
import random
import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from datetime import datetime

router = APIRouter()
logger = logging.getLogger("api")

# Check if Loki is available
loki_available = False
try:
    loki_available = True
except ImportError:
    pass

@router.get("/metrics", response_class=PlainTextResponse)
async def metrics():
    """Prometheus metrics endpoint"""
    return PlainTextResponse(generate_latest().decode(), media_type=CONTENT_TYPE_LATEST)

@router.get("/loki-status")
def loki_status():
    """Check if Loki logging is operational"""
    # Get the real URL that was used for Loki configuration
    loki_url = "http://host.docker.internal:3100/loki/api/v1/push" if sys.platform in ["darwin", "win32"] else "http://localhost:3100/loki/api/v1/push"
    return {
        "loki_enabled": loki_available,
        "loki_url": loki_url if loki_available else None,
        "timestamp": datetime.now().isoformat()
    }

@router.get("/error")
async def throw_error(type: str = None):
    """
    Test endpoint to generate different types of errors
    
    Parameters:
    - type: Type of error to generate (value, key, type, runtime). If not specified, a random error will be thrown.
    """
    if os.getenv("ENV", "development").lower() != "development":
        raise HTTPException(status_code=403, detail="Access denied")

    error_type = type or random.choice(["value", "key", "type", "runtime"])
    logger.error(f"500 - 🔴 Triggered {error_type} error", extra={"status_code": 500})

    match error_type:
        case "value": 
            raise ValueError("Boom! ValueError triggered.")
        case "key": 
            raise KeyError("Oops! KeyError triggered.")
        case "type": 
            raise TypeError("Bruh! TypeError triggered.")
        case _: 
            raise RuntimeError("Chaos! RuntimeError triggered.")