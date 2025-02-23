from kafka import KafkaConsumer, KafkaProducer
import redis
import json

KAFKA_BROKER = "localhost:9092"
CONTROL_TOPIC = "pr-routing-dynamicrouter-control-channel"
MESSAGE_TOPIC = "pr-routing-dynamicrouter-message-channel"

# Conexión a Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Configurar consumidores y productores de Kafka
consumer_control = KafkaConsumer(
    CONTROL_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

consumer_message = KafkaConsumer(
    MESSAGE_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Procesar mensajes de configuración
for msg in consumer_control:
    data = msg.value
    redis_client.set(data["id"], json.dumps(data["conditions"]))
    print(f"Guardando reglas para {data['id']}: {data['conditions']}")

# Procesar mensajes de enrutamiento
for msg in consumer_message:
    message_data = msg.value
    print(f"Procesando mensaje: {message_data}")

    # Buscar destinatarios que coincidan con la condición
    for key in redis_client.keys():
        conditions = json.loads(redis_client.get(key))
        if all(message_data.get(k) == v for k, v in conditions.items()):
            producer.send(key, message_data)
            print(f"Mensaje enviado a {key}: {message_data}")

producer.flush()
