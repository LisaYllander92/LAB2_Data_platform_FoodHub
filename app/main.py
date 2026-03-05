import json

from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager

from kafka import KafkaProducer
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row

import os

from starlette import status


DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Kafka Setup
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
#PRODUCTS_TOPIC = os.getenv("PRODUCTS_TOPIC", "products.created")

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)