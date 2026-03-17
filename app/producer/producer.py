from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import logging
from app.services.ingredient_service import has_ingredient
import os

log = logging.getLogger(__name__)

_producer = None  # modulnivå — bara en variabel, ingen anslutning


##Fix to make sure kafka is initialized when needed and not before it's ready.

def get_producer() -> KafkaProducer:
    global _producer
    if _producer is None:
        _producer = KafkaProducer(
            bootstrap_servers=[os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")], # ansluter till kafka-container
            value_serializer=lambda m: json.dumps(m).encode('utf-8'), # omvandlar automatiskt data till bytes vid varje send
            retries=5 # försöker upp till 5 gånger om något går fel.
        )

    return _producer


def send_recipes(data):
    if isinstance(data, str):
        df = has_ingredient(data)
        payload = df.to_dict('records')
    elif isinstance(data, dict):
        payload = [data] if not isinstance(data, list) else data
    else:
        log.error(f"Unexpected format to 'send_recipe': {type(data)}")
        return

    # Send to Kafka
    try:
        producer = get_producer()
        # Vi skickar 'payload' som nu garanterat är en lista/dict som kan JSON-serialiseras
        future = producer.send('recipe-request', value=payload)
        record_metadata = future.get(timeout=2)
        log.info(f"Message sent to {record_metadata.topic}, offset {record_metadata.offset}")
    except KafkaError:
        log.exception("Failed to send message to Kafka")

"""
Producer är som en avsändare. Den tar recept från vår sökfunktion och skickar dem som ett paket till Kafka. 
Kafka tar emot paketet och lägger det i en brevlåda som heter recipe-result.
Sedan väntar den på att Kafka bekräftar att paketet kom fram – om inte försöker den igen upp till 5 gånger.
"""


