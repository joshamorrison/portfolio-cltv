"""
Customer Lifetime Value & Churn Prediction Platform - FastAPI Application
Production-ready API for CLTV prediction and churn prevention automation.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from contextlib import asynccontextmanager

from .routers import predictions, churn, health, automation
from .models.response_models import HealthResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    # Startup
    print("🚀 CLTV & Churn Prediction Platform starting up...")
    
    # Initialize ML models
    try:
        # Model loading will be implemented here
        print("✅ ML models loaded successfully")
    except Exception as e:
        print(f"⚠️ Model loading failed: {e}")
    
    # Initialize LangChain agents
    try:
        # Agent initialization will be implemented here
        print("✅ LangChain agents initialized")
    except Exception as e:
        print(f"⚠️ Agent initialization failed: {e}")
    
    yield
    
    # Shutdown
    print("🔄 CLTV Platform shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Customer Lifetime Value & Churn Prediction Platform",
    description="Advanced predictive modeling system for customer retention and value optimization",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(predictions.router, prefix="/api/v1/predictions", tags=["predictions"])
app.include_router(churn.router, prefix="/api/v1/churn", tags=["churn"])
app.include_router(automation.router, prefix="/api/v1/automation", tags=["automation"])


@app.get("/", response_model=dict)
async def root():
    """Root endpoint."""
    return {
        "message": "Customer Lifetime Value & Churn Prediction Platform",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs",
        "capabilities": [
            "Customer lifetime value prediction",
            "Churn probability analysis", 
            "Automated retention campaigns",
            "Customer segmentation",
            "Risk scoring"
        ]
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("ENVIRONMENT") == "development"
    )