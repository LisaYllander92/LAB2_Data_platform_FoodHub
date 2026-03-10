import json
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from kafka import KafkaProducer
from psycopg_pool import ConnectionPool
from pathlib import Path
import pandas as pd
from app.services.recipe_service import has_ingredient
from psycopg.rows import dict_row

matches = has_ingredient("avocado")


DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

pool = ConnectionPool(DATABASE_URL)

app = FastAPI(title="FoodHub API")

@app.get("/")
def read_root():
    return {"message": "FoodHub is running"}

@app.get("/recipes/search")
def search_by_ingredient(ingredient: str):
    matches = has_ingredient(ingredient)
    return matches.to_dict(orient="records")