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
REDIS_STREAM = "ofertas_usuarios"
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
        KAFKA_TOPIC, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, group_id="marketing-group"
    )
    await consumer.start()
    try:
        async for message in consumer:
            data = json.loads(message.value)
            usuario_id = data["usuario_id"]
            mensaje = data["mensaje"]

            # Verificar si el mensaje ya fue procesado
            if redis_client.hexists(REDIS_PROCESSED_KEY, usuario_id):
                print(f"Mensaje ya procesado para el usuario {usuario_id}. Descartando...")
                continue

            # Seleccionar el canal prioritario
            canal = seleccionar_canal_prioritario(usuario_id)

            # Intentar enviar el mensaje por el canal seleccionado
            if enviar_mensaje_por_canal(canal, usuario_id, mensaje):
                # Marcar el mensaje como procesado en Redis
                redis_client.hset(REDIS_PROCESSED_KEY, usuario_id, "entregado")
                print(f"Mensaje entregado a {usuario_id} por {canal.value}.")
            else:
                # Reintentar por otro canal en caso de fallo
                reintentar_por_otro_canal(usuario_id, mensaje)
    finally:
        await consumer.stop()

def seleccionar_canal_prioritario(usuario_id: str) -> Canal:
    """
    Selecciona el canal prioritario basado en reglas de negocio.
    Aquí puedes implementar lógica más compleja si es necesario.
    """
    # Ejemplo simple: priorizar WhatsApp, luego SMS, luego Email
    if usuario_usa_whatsapp(usuario_id):
        return Canal.WHATSAPP
    elif usuario_usa_sms(usuario_id):
        return Canal.SMS
    else:
        return Canal.EMAIL

def usuario_usa_whatsapp(usuario_id: str) -> bool:
    """
    Simula la verificación de si un usuario usa WhatsApp.
    """
    # Aquí puedes implementar lógica real, como consultar una base de datos.
    return True  # Ejemplo: todos los usuarios usan WhatsApp

def usuario_usa_sms(usuario_id: str) -> bool:
    """
    Simula la verificación de si un usuario usa SMS.
    """
    # Aquí puedes implementar lógica real, como consultar una base de datos.
    return False  # Ejemplo: ningún usuario usa SMS

def enviar_mensaje_por_canal(canal: Canal, usuario_id: str, mensaje: str) -> bool:
    """
    Simula el envío de un mensaje por un canal específico.
    Retorna True si el mensaje fue entregado, False en caso de fallo.
    """
    print(f"Intentando enviar mensaje a {usuario_id} por {canal.value}...")
    # Simulación de envío (aquí puedes integrar APIs reales de Email, SMS, WhatsApp)
    if canal == Canal.WHATSAPP:
        return True  # Simulación: WhatsApp siempre funciona
    elif canal == Canal.SMS:
        return False  # Simulación: SMS falla
    else:
        return True  # Simulación: Email siempre funciona

def reintentar_por_otro_canal(usuario_id: str, mensaje: str):
    """
    Reintenta enviar el mensaje por otro canal en caso de fallo.
    """
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
    redis_client.delete(stream_key)  # Eliminar las ofertas una vez entregadas
    return {"ofertas": [oferta[1] for oferta in ofertas]}

@app.get("/metricas/")
async def obtener_metricas():
    """
    Obtiene métricas de envíos, entregas y fallos.
    """
    total_mensajes = redis_client.hlen(REDIS_PROCESSED_KEY)
    entregados = sum(1 for estado in redis_client.hvals(REDIS_PROCESSED_KEY) if estado == "entregado")
    fallos = total_mensajes - entregados
    return {
        "total_mensajes": total_mensajes,
        "entregados": entregados,
        "fallos": fallos
    }