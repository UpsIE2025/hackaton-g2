from kafka import KafkaProducer
import json
import time

KAFKA_BROKER = "localhost:9092"
CONTROL_TOPIC = "pr-routing-dynamicrouter-control-channel"
MESSAGE_TOPIC = "pr-routing-dynamicrouter-message-channel"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Simulación de destinatarios registrándose
destinatarios = [
    {"id": "dest-1", "conditions": {"type": "order"}},
    {"id": "dest-2", "conditions": {"type": "payment"}}
]

for dest in destinatarios:
    producer.send(CONTROL_TOPIC, dest)
    print(f"Registrando destinatario: {dest}")
    time.sleep(1)

# Enviar mensajes de prueba
mensajes = [
    {"id": 1, "type": "order", "content": "Nueva orden creada"},
    {"id": 2, "type": "payment", "content": "Pago recibido"}
]

for msg in mensajes:
    producer.send(MESSAGE_TOPIC, msg)
    print(f"Enviando mensaje: {msg}")
    time.sleep(1)

producer.flush()
