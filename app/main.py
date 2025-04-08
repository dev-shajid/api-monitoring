import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.logging import setup_logging
from app.core.middleware import setup_middleware
from app.routes.base import router as base_router
from app.routes.products import router as items_router
from app.routes.monitoring import router as monitoring_router

# Setup logging
logger = setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("🚀 Application startup complete")
    yield
    logger.info("🛑 Application shutdown initiated")

"""Create and configure the FastAPI application"""
app = FastAPI(
    title="E-Commerce API with Monitoring",
    description="FastAPI application with Prometheus and Loki integration",
    version="1.0.0",
    lifespan=lifespan
)

# Setup middleware
setup_middleware(app)

# Include routers
app.include_router(base_router)
app.include_router(items_router, prefix="/products", tags=["Products"])
app.include_router(monitoring_router, tags=["Monitoring"])
    

if __name__ == "__main__":
    logger.info("🔥 Launching FastAPI app...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)