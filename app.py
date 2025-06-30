

from fastapi import FastAPI
from routers import summarizer_routes

# Create FastAPI app instance
app = FastAPI(
    title="Investor Profiling API",
    description="APIs for extracting and summarizing investor profile data",
    version="1.0.0"
)

# Include the summarizer routes
app.include_router(summarizer_routes.router)
