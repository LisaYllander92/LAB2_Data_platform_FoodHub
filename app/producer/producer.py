from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import logging
from app.services.ingredient_service import has_ingredient
import os

log = logging.getLogger(name)

_producer = None  # modulnivå — bara en variabel, ingen anslutning

def get_producer():
    global _producer
    if _producer is None:
        _producer = KafkaProducer(
            bootstrap_servers=[os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")],
            value_serializer=lambda m: json.dumps(m).encode('utf-8'),
            retries=5
        )
    return _producer

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


def send_recipes(search: str):
    df = has_ingredient(search)

    try:
        producer = get_producer()
        future = producer.send('recipe-request', value=df.to_dict( 'records'))  # Skickar recepten till Kafka-topicen, omvandlar DataFrame till en lista av dicts — ett recept per dict.
        record_metadata = future.get(timeout=2) # Väntar på bekräftelse från Kafka (max 2 sekunder). Om det lyckas loggas topic och offset. Om något går fel loggas felet.
        log.info(f"Message sent to {record_metadata.topic}, offset {record_metadata.offset}")
    except KafkaError:
        log.exception("Failed to send message to Kafka")

"""
Producer är som en avsändare. Den tar recept från vår sökfunktion och skickar dem som ett paket till Kafka. 
Kafka tar emot paketet och lägger det i en brevlåda som heter recipe-result.
Sedan väntar den på att Kafka bekräftar att paketet kom fram – om inte försöker den igen upp till 5 gånger.
"""


