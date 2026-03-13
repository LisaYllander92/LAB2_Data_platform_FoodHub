import os
import json
from kafka import KafkaConsumer
from psycopg.types.json import Json
from app.database import pool

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TOPIC = "recipe-request"
GROUP_ID = "print-request"

def main():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=GROUP_ID,
        auto_offset_reset="latest",
        value_deserializer=lambda b: json.loads(b.decode("utf-8")),
        key_deserializer=lambda b: b.decode("utf-8") if b else None,
    )

    for msg in consumer:
        print("Received:", msg.value)
        try:
            with pool.connection() as conn:
                conn.execute(
                    "INSERT INTO staging_recipes (raw_data) VALUES (%s)",
                    (Json(msg.value),)
                )
        except Exception as e:
            print(f"Failed to insert message: {e}")

if __name__ == "__main__":
    main()