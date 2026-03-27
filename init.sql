CREATE TABLE IF NOT EXISTS staging_recipes (
    id SERIAL PRIMARY KEY,
    raw_data TEXT NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS curated_recipes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(250) NOT NULL UNIQUE,
    image TEXT,
    cooking_minutes INT,
    servings INT,
    instructions TEXT,
    ingredients TEXT,
    ingredients_normalized TEXT,
    cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS search_log (
    id SERIAL PRIMARY KEY,
    query VARCHAR(255) NOT NULL,
    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);