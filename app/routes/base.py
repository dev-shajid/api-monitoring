import socket
from datetime import datetime
from fastapi import APIRouter, HTTPException
import logging

router = APIRouter()
logger = logging.getLogger("api")

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
def health_check():
    """API health check endpoint"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "hostname": socket.gethostname()
    }