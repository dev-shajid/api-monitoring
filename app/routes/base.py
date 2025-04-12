import socket
from datetime import datetime
from fastapi import APIRouter, HTTPException
import logging

from prometheus_client import Counter, Gauge
import random

router = APIRouter()
logger = logging.getLogger("api")

# Custom metrics for health endpoint
HEALTH_CHECK_COUNTER = Counter(
    "api_health_check_total", 
    "Total number of health check calls"
)

HEALTH_CHECK_LATENCY = Gauge(
    "api_health_check_latency_ms", 
    "Current health check latency in milliseconds"
)

SYSTEM_HEALTH_SCORE = Gauge(
    "api_system_health_score",
    "Current system health score (0-100)"
)


@router.get("/", tags=["Base"])
def root():
    """API root endpoint"""
    logger.info("🏠 Root endpoint hit")
    return {
        "message": "E-Commerce API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@router.get("/health", tags=["Base"])
async def health_check():
    """API health check endpoint with custom metrics"""
    try:
        # Simulate some random health metrics
        response_time = random.uniform(0.1, 2.0)
        health_score = random.uniform(80, 100)
        
        # Update our custom metrics
        HEALTH_CHECK_COUNTER.inc()
        HEALTH_CHECK_LATENCY.set(response_time * 1000)
        SYSTEM_HEALTH_SCORE.set(health_score)
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "response_time_ms": round(response_time * 1000, 2),
                "health_score": round(health_score, 2)
            }
        }
    except Exception as e:
        logger.error(f"❌ Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Health check failed")