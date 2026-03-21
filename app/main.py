"""Main FastAPI application entry point for the FoodHub API.

Initializes the application, registers routers for specific API endpoints, 
and sets up global exception handling.
"""
import os
import traceback
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.recipe_routes import router as recipe_router

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

app = FastAPI(title="FoodHub API")
app.include_router(recipe_router, prefix="/api")


@app.get("/")
def read_root():
    """Health check endpoint to verify that the API is up and running."""
    return {"message": "FoodHub is running"}


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Global exception handler to return formatted JSON responses.

    Args:
        request (Request): The incoming HTTP request.
        exc (Exception): The unhandled exception that was raised.

    Returns:
        JSONResponse: A 500 error response containing the error details and traceback.
    """
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "traceback": traceback.format_exc()}
    )