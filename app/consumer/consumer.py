import pandas as pd
import os
import json
import re
import asyncio
from kafka import KafkaConsumer
from psycopg.types.json import Json
from app.database import pool
from app.services.recipe_service import search_pipeline

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TOPIC = "recipe-request"
GROUP_ID = "print-request"

def main():
    import time

    consumer = None
    for attempt in range(10):
        try:
            consumer = KafkaConsumer(
                TOPIC,
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                group_id=GROUP_ID,
                auto_offset_reset="latest",
                value_deserializer=lambda b: json.loads(b.decode("utf-8")),
                key_deserializer=lambda b: b.decode("utf-8") if b else None,
            )
            print("Connected to Kafka!")
            break
        except Exception as e:
            print(f"Kafka not ready, retrying... ({attempt + 1}/10): {e}")
            time.sleep(5)

    if consumer is None:
        print("Could not connect to Kafka after 10 tries.")
        return


    # ... inuti din consumer-loop:
    # Inuti din for-loop i consumer.py:
    for msg in consumer:
        recipes_list = msg.value  # Detta är nu en lista med recept-objekt
        if not isinstance(recipes_list, list):
            recipes_list = [recipes_list]

        for recipe in recipes_list:
            try:
                raw_instruction = recipe.get("instructions") or ""
                clean_instruction = re.sub(r'<[^>]*>', '', raw_instruction).strip()

                with pool.connection() as conn:
                    with conn.cursor() as cur:
                        # STEG A: Spara rådata i Staging (för historik/backup)
                        cur.execute(
                            "INSERT INTO staging_recipes (raw_data) VALUES (%s) RETURNING id",
                            (json.dumps(recipe),)
                        )

                        # STEG B: Spara i Curated (Den snygga tabellen)
                        cur.execute(
                            """
                            INSERT INTO curated_recipes (title, image, cooking_minutes, servings, instruction)
                            VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING RETURNING id
                            """,
                            (
                                recipe.get("title"),
                                recipe.get("image"),
                                recipe.get("cooking_minutes", 0),
                                recipe.get("servings", 0),
                                clean_instruction
                            )
                        )
                        res = cur.fetchone()
                        if res:
                            #new_recipe_id = res[0]
                            print(f"Success: Recept '{recipe.get('title')}' cureted & cleaned!")

                    conn.commit()
            except Exception as e:
                print(f"Error under curation: {e}")


if __name__ == "__main__":
    main()

#TOPIC — ändrat till "recipe-requests" (med s)
#import asyncio + asyncio.run() — för att köra den asynkrona search_pipeline() från synkron kod
#query = msg.value.get("query") if isinstance(msg.value, dict) else msg.value — hanterar om meddelandet är ett JSON-objekt {"query": "avocado"} eller bara en sträng "avocado"
