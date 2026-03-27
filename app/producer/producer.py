"""Kafka producer for sending recipe data to the message broker.

Acts as a sender that takes recipes from the search function, formats them, 
and securely delivers them to the Kafka topic. Includes automatic JSON 
serialization and connection retries to ensure message delivery.
"""
import os
import json
import logging
from kafka import KafkaProducer
from kafka.errors import KafkaError

from app.services.ingredient_service import has_ingredient

log = logging.getLogger(__name__)

_producer = None


def get_producer() -> KafkaProducer:
    """Lazily initialize and return the Kafka producer instance.

    Creates the producer only when first needed, configuring the connection 
    to the Kafka container, automatic JSON serialization to bytes, and 
    up to 5 delivery retries.
    """
    global _producer
    if _producer is None:
        _producer = KafkaProducer(
            bootstrap_servers=[os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")],
            value_serializer=lambda m: json.dumps(m).encode('utf-8'),
            retries=5
        )

    return _producer


def send_recipes(data):
    """Format the input data and send it as a message to the Kafka topic.

    Handles strings (by fetching ingredients to a dataframe), lists, and dicts. 
    Logs an error if the data format is unexpected or empty.
    """
    if isinstance(data, str):
        df = has_ingredient(data)
        payload = df.to_dict('records')
    elif isinstance(data, list):
        payload = data
    elif isinstance(data, dict):
        payload = [data]
    else:
        log.error(f"Unexpected format to 'send_recipe': {type(data)}")
        return

    if not payload:
        log.info("No data to send to Kafka (empty list)")
        return

    try:
        producer = get_producer()
        future = producer.send('recipe-request', value=payload)
        record_metadata = future.get(timeout=2)
        log.info(f"Message sent to {record_metadata.topic}, offset {record_metadata.offset}")
    except KafkaError:
        log.exception("Failed to send message to Kafka")