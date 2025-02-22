from kafka import KafkaConsumer
import redis
import json

# Conectar con Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Definir canales que el consumidor escuchará
topics = ["pr-channel-datatype-usuarios", "pr-channel-datatype-productos", "pr-channel-datatype-transacciones"]

# Configurar el consumidor de Kafka
consumer = KafkaConsumer(
    *topics,
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

print("🎧 Escuchando los canales...")

for message in consumer:
    topic = message.topic
    data = message.value

    # Almacenar en Redis
    redis_client.rpush(topic, json.dumps(data))
    print(f"✅ Datos recibidos en {topic} y almacenados en Redis: {data}")
