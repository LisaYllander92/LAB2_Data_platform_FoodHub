from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import logging # för att logga vad som händer, istället för print typ
from app.services.recipe_service import has_ingredient

log = logging.getLogger(__name__) # Skapar en logger kopplad till denna fil — används för att skriva ut meddelanden i terminalen.

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'], # ansluter till kafka-container
    value_serializer=lambda m: json.dumps(m).encode('utf-8'), # omvandlar automatiskt data till bytes vid varje send
    retries=5 # försöker upp till 5 gånger om något går fel.
)
def send_recipes(search: str):
    df = has_ingredient(search)
    future = producer.send('recipe-result', value=df.to_dict('records')) # Skickar recepten till Kafka-topicen, omvandlar DataFrame till en lista av dicts — ett recept per dict.
    try:
        record_metadata = future.get(timeout=10) # Väntar på bekräftelse från Kafka (max 10 sekunder). Om det lyckas loggas topic och offset. Om något går fel loggas felet.
        log.info(f"Message sent to {record_metadata.topic}, offset {record_metadata.offset}")
    except KafkaError:
        log.exception("Failed to send message to Kafka")

"""
Producer är som en avsändare. Den tar recept från vår sökfunktion och skickar dem som ett paket till Kafka. 
Kafka tar emot paketet och lägger det i en brevlåda som heter recipe-result.
Sedan väntar den på att Kafka bekräftar att paketet kom fram – om inte försöker den igen upp till 5 gånger.
"""


