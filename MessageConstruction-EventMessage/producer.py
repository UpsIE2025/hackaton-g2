from kafka import KafkaProducer
import json

KAFKA_BROKER = "localhost:9092"
TOPIC = "nuevo-evento"

def create_kafka_producer():
    return KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

def send_event(event):
    producer = create_kafka_producer()
    producer.send(TOPIC, event)
    producer.flush()
    print(f"Evento enviado: {event}")

if __name__ == "__main__":
    event = {"id": 1, "mensaje": "Pedido creado", "usuario": "cliente_123"}
    send_event(event)
