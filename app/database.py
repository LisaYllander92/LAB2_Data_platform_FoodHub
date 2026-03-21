"""Database connection configuration and pool initialization.

Loads database credentials from environment variables and establishes
a connection pool using psycopg_pool for the PostgreSQL database.
"""
import os
from psycopg_pool import ConnectionPool

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

pool = ConnectionPool(DATABASE_URL)