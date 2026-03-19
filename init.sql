CREATE TABLE IF NOT EXISTS staging_recipes (
    id SERIAL PRIMARY KEY,
    raw_data TEXT NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS curated_recipe (
    id SERIAL PRIMARY KEY,
    title VARCHAR(250) NOT NULL UNIQUE, -- Lade till UNIQUE här
    image TEXT,
    cooking_minutes INT,
    servings INT,
    instruction TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE curated_recipe ADD COLUMN ingredients TEXT;

CREATE TABLE IF NOT EXISTS ingredients (
    ingred_id SERIAL PRIMARY KEY,
    ingred_name VARCHAR(255) NOT NULL,
    category VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS recipe_ingredients (
    ingred_id INT REFERENCES ingredients(ingred_id),
    recipe_id INT REFERENCES curated_recipe(id),
    amount INT,
    unit VARCHAR(255),
    PRIMARY KEY (ingred_id, recipe_id)
);

CREATE TABLE IF NOT EXISTS recipe_steps (
    step_id SERIAL PRIMARY KEY,
    recipe_id INT REFERENCES curated_recipe(id), 
    step_nr INT NOT NULL,
    instruction TEXT NOT NULL,
    timer_minutes INT
);

CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL,
    password VARCHAR(250) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS favorites (
    user_id INT REFERENCES users(user_id),
    recipe_id INT REFERENCES curated_recipe(id),
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, recipe_id)
);

CREATE TABLE IF NOT EXISTS search_events (
    search_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS search_event_ingredients (
    search_id INT REFERENCES search_events(search_id),
    ingred_id INT REFERENCES ingredients(ingred_id),
    PRIMARY KEY (search_id, ingred_id)
);