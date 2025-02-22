from fastapi import FastAPI
from pydantic import BaseModel
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import redis
import json
import asyncio

app = FastAPI()

# Configuración de Kafka y Redis
KAFKA_TOPIC = "js-channel-oferta"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_STREAM = "ofertas_usuarios"

# Cliente Redis
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# Modelo de Oferta
class Oferta(BaseModel):
    usuario_id: str
    mensaje: str

to_bytes = lambda x: json.dumps(x).encode('utf-8')

@app.on_event("startup")
async def startup_event():
    global producer
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    asyncio.create_task(consume_messages())

@app.on_event("shutdown")
async def shutdown_event():
    await producer.stop()

@app.post("/enviar_oferta/")
async def enviar_oferta(oferta: Oferta):
    await producer.send(KAFKA_TOPIC, to_bytes(oferta.dict()))
    return {"status": "Oferta enviada a Kafka"}

async def consume_messages():
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, group_id="marketing-group"
    )
    await consumer.start()
    try:
        async for message in consumer:
            data = json.loads(message.value)
            redis_client.xadd(REDIS_STREAM + ":" + data["usuario_id"], {"mensaje": data["mensaje"]})
    finally:
        await consumer.stop()

@app.get("/obtener_ofertas/{usuario_id}")
async def obtener_ofertas(usuario_id: str):
    stream_key = REDIS_STREAM + ":" + usuario_id
    ofertas = redis_client.xrange(stream_key)
    redis_client.delete(stream_key)  # Eliminar las ofertas una vez entregadas
    return {"ofertas": [oferta[1] for oferta in ofertas]}
