from kafka import KafkaConsumer, KafkaProducer
import redis
import json

KAFKA_BROKER = "localhost:9092"
INPUT_TOPIC = "nuevo-evento"
OUTPUT_TOPIC = "evento-procesado"
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

def create_kafka_consumer():
    return KafkaConsumer(
        INPUT_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    )

def create_kafka_producer():
    return KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

def create_redis_client():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

def process_event(event):
    print(f"Procesando evento: {event}")
    return {"id": event["id"], "mensaje": f"{event['mensaje']} - PROCESADO"}

def consume_events():
    consumer = create_kafka_consumer()
    producer = create_kafka_producer()
    redis_client = create_redis_client()

    for message in consumer:
        event = message.value
        redis_client.set(f"evento:{event['id']}", json.dumps(event))
        print(f"Evento almacenado en Redis: {event}")

        processed_event = process_event(event)
        producer.send(OUTPUT_TOPIC, processed_event)
        producer.flush()
        print(f"Evento procesado enviado a Kafka: {processed_event}")

if __name__ == "__main__":
    consume_events()
