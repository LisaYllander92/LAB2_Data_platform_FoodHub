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

    for msg in consumer:
        print("Received:", msg.value)
        try:
            # 1. Spara söktermen i staging
            with pool.connection() as conn:
                conn.execute(
                    "INSERT INTO staging_recipes (raw_data) VALUES (%s)",
                    (Json(msg.value),)
                )
                # 2. Anropa Spoonacular och spara resultatet
                query = msg.value.get("query") if isinstance(msg.value, dict) else msg.value
                result = asyncio.run(search_pipeline(query, number=5, offset=0))
                print("Pipeline result:", result)

        except Exception as e:
            print(f"Failed to insert message: {e}")

if __name__ == "__main__":
    main()

#TOPIC — ändrat till "recipe-requests" (med s)
#import asyncio + asyncio.run() — för att köra den asynkrona search_pipeline() från synkron kod
#query = msg.value.get("query") if isinstance(msg.value, dict) else msg.value — hanterar om meddelandet är ett JSON-objekt {"query": "avocado"} eller bara en sträng "avocado"
