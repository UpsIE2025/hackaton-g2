from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import redis
import json
import asyncio
from enum import Enum

app = FastAPI()

# Configuración de Kafka y Redis
KAFKA_TOPIC = "js-channel-oferta"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_STREAM = "ofertas_usuarios2"
REDIS_PROCESSED_KEY = "mensajes_procesados"

# Cliente Redis
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# Modelo de Oferta
class Oferta(BaseModel):
    usuario_id: str
    mensaje: str

# Enum para canales de envío
class Canal(Enum):
    EMAIL = "email"
    SMS = "sms"
    WHATSAPP = "whatsapp"

# Función para serializar a bytes
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
    # Verificar si el mensaje ya fue procesado
    if redis_client.hexists(REDIS_PROCESSED_KEY, oferta.usuario_id):
        raise HTTPException(status_code=400, detail="El mensaje ya fue procesado para este usuario.")
    
    # Enviar el mensaje a Kafka
    await producer.send(KAFKA_TOPIC, to_bytes(oferta.dict()))
    return {"status": "Oferta enviada a Kafka"}

async def consume_messages():
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, group_id="suscribechanel-group"
    )
    await consumer.start()
    try:
        async for message in consumer:
            data = json.loads(message.value)
            usuario_id = data["usuario_id"]
            mensaje = data["mensaje"]

           
            if redis_client.hexists(REDIS_PROCESSED_KEY, usuario_id):
                print(f"Mensaje ya procesado para el usuario {usuario_id}. Descartando...")
                continue

          
            canal = seleccionar_canal_prioritario(usuario_id)

           
            if enviar_mensaje_por_canal(canal, usuario_id, mensaje):
              
                redis_client.hset(REDIS_PROCESSED_KEY, usuario_id, "entregado")
                print(f"Mensaje entregado a {usuario_id} por {canal.value}.")
            else:
             
                reintentar_por_otro_canal(usuario_id, mensaje)
    finally:
        await consumer.stop()

def seleccionar_canal_prioritario(usuario_id: str) -> Canal:
 
    if usuario_usa_whatsapp(usuario_id):
        return Canal.WHATSAPP
    elif usuario_usa_sms(usuario_id):
        return Canal.SMS
    else:
        return Canal.EMAIL

def usuario_usa_whatsapp(usuario_id: str) -> bool:
   
    return True 

def usuario_usa_sms(usuario_id: str) -> bool:
    
    return False  #

def enviar_mensaje_por_canal(canal: Canal, usuario_id: str, mensaje: str) -> bool:
    
    print(f"Intentando enviar mensaje a {usuario_id} por {canal.value}...")
   
    if canal == Canal.WHATSAPP:
        return True  
    elif canal == Canal.SMS:
        return False  
    else:
        return True  

def reintentar_por_otro_canal(usuario_id: str, mensaje: str):
    
    canales = [Canal.WHATSAPP, Canal.SMS, Canal.EMAIL]
    for canal in canales:
        if enviar_mensaje_por_canal(canal, usuario_id, mensaje):
            redis_client.hset(REDIS_PROCESSED_KEY, usuario_id, "entregado")
            print(f"Mensaje reenviado a {usuario_id} por {canal.value}.")
            return
    print(f"No se pudo entregar el mensaje a {usuario_id} por ningún canal.")

@app.get("/obtener_ofertas/{usuario_id}")
async def obtener_ofertas(usuario_id: str):
    stream_key = REDIS_STREAM + ":" + usuario_id
    ofertas = redis_client.xrange(stream_key)
    print([oferta[1] for oferta in ofertas])   
    redis_client.delete(stream_key) 
    print('------------')
    return {"ofertas": [oferta[1] for oferta in ofertas]}

@app.get("/metricas/")
async def obtener_metricas():
   
    total_mensajes = redis_client.hlen(REDIS_PROCESSED_KEY)
    entregados = sum(1 for estado in redis_client.hvals(REDIS_PROCESSED_KEY) if estado == "entregado")
    fallos = total_mensajes - entregados
    return {
        "total_mensajes": total_mensajes,
        "entregados": entregados,
        "fallos": fallos
    }