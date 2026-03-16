import json
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from kafka import KafkaProducer
from pathlib import Path
import pandas as pd
from app.producer.producer import send_recipes
from app.services.ingredient_service import has_ingredient
from app.api.recipe_routes import router as recipe_router
from app.services.recipe_service import has_ingredient
from psycopg.rows import dict_row
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import traceback

"""####### dev search ######## - for now"""
## has_ingredient("avocado", df=) to use DF instead of mock/clean-json
## has_ingredient("avocado", save=false) to not make a json of the output
#matches = has_ingredient("avocado")

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
app = FastAPI(title="FoodHub API")

app.include_router(recipe_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "FoodHub is running"}

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "traceback": traceback.format_exc()}
    )

"""@app.get("/recipes/search")
def search_by_ingredient(ingredient: str):
    matches = has_ingredient(ingredient)
    from app.producer.producer import send_recipes
    send_recipes(ingredient)
    return matches.to_dict(orient="records")"""