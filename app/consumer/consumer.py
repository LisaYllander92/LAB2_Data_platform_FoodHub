import pandas as pd
import os
import json
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
    for msg in consumer:
        print("Received:", msg.value)
        try:
            # 1. Konvertera till JSON-sträng.
            # Vi använder en funktion (default) för att tvinga NaN till null
            clean_json = json.dumps(msg.value,
                                    default=lambda o: None if isinstance(o, float) and pd.isna(o) else o).replace('NaN',
                                                                                                                  'null')

            # 2. Ladda tillbaka till ett rent objekt
            clean_data = json.loads(clean_json)

            with pool.connection() as conn:
                conn.execute(
                    "INSERT INTO staging_recipes (raw_data) VALUES (%s)",
                    (Json(clean_data),)
                )
                conn.commit()
                print("Success: Data sparad i staging_recipes!")

        except Exception as e:
            print(f"Failed to insert message: {e}")

if __name__ == "__main__":
    main()

#TOPIC — ändrat till "recipe-requests" (med s)
#import asyncio + asyncio.run() — för att köra den asynkrona search_pipeline() från synkron kod
#query = msg.value.get("query") if isinstance(msg.value, dict) else msg.value — hanterar om meddelandet är ett JSON-objekt {"query": "avocado"} eller bara en sträng "avocado"
