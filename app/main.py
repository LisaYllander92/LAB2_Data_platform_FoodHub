import json
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from kafka import KafkaProducer
from pathlib import Path
import pandas as pd
from app.producer.producer import send_recipes
from app.services.recipe_service import has_ingredient
from psycopg.rows import dict_row

"""####### dev search ######## - for now"""
matches = has_ingredient("avocado")

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
app = FastAPI(title="FoodHub API")

@app.get("/")
def read_root():
    return {"message": "FoodHub is running"}

@app.get("/recipes/search")
def search_by_ingredient(ingredient: str):
    matches = has_ingredient(ingredient)
    send_recipes(ingredient)
    return matches.to_dict(orient="records")