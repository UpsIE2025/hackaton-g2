from kafka import KafkaConsumer
import json

KAFKA_BROKER = "localhost:9092"
TOPIC = "dest-1"  # Cambiar según el destinatario

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

print(f"Escuchando en {TOPIC}...")
for msg in consumer:
    print(f"Mensaje recibido: {msg.value}")
