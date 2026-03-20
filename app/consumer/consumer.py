import os
import json
import math
from kafka import KafkaConsumer
from app.database import pool

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TOPIC = "recipe-request"
GROUP_ID = "print-request"

# NaN/Inf cleaner
def clean_json(obj):
    """Recursively replaces NaN/Inf with None for JSON compatibility."""
    if isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
        return None
    if isinstance(obj, dict):
        return {k: clean_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean_json(i) for i in obj]
    return obj

def main():
    import time
    # --- Kafka connection with retry logic ---
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


    # Ändrad!
    # --- Save incoming messages to staging ---
    # Curated saving is handled by recipe_service.py after Spoonacular transform
    for msg in consumer:
            try:
                with pool.connection() as conn:
                    conn.execute(
                        "INSERT INTO staging_recipes (raw_data) VALUES (%s)",
                        (json.dumps(clean_json(msg.value)),)
                    )
                    print("Saved to staging!")
            except Exception as e:
                print(f"Failed to insert to staging: {e}")

if __name__ == "__main__":
    main()
