from aiokafka import AIOKafkaConsumer
import redis
import json
import asyncio


KAFKA_TOPIC = "js-construction-oferta"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PROCESSED_KEY = "mensajes_procesados"


redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

async def consume_messages():
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, group_id="notificaciones-group"
    )
    await consumer.start()
    try:
        async for message in consumer:
            data = json.loads(message.value)
            usuario_id = data["usuario_id"]
            mensaje = data["mensaje"]
            canal_prioritario = data["canal_prioritario"]
            intentos = data["intentos"]

          
            if redis_client.hexists(REDIS_PROCESSED_KEY, usuario_id):
                print(f"Mensaje ya procesado para el usuario {usuario_id}. Descartando...")
                continue

        
            if enviar_mensaje_por_canal(canal_prioritario, usuario_id, mensaje):
               
                redis_client.hset(REDIS_PROCESSED_KEY, usuario_id, "entregado")
                print(f"Mensaje entregado a {usuario_id} por {canal_prioritario}.")
            else:
                
                reintentar_por_otro_canal(usuario_id, mensaje, intentos)
    finally:
        await consumer.stop()

def enviar_mensaje_por_canal(canal: str, usuario_id: str, mensaje: str) -> bool:
   
    print(f"Intentando enviar mensaje a {usuario_id} por {canal}...")
  
    if canal == "whatsapp":
        return True  
    elif canal == "sms":
        return False  
    else:
        return True 

def reintentar_por_otro_canal(usuario_id: str, mensaje: str, intentos: int):
  
    canales = ["whatsapp", "sms", "email"]
    for canal in canales:
        if enviar_mensaje_por_canal(canal, usuario_id, mensaje):
            redis_client.hset(REDIS_PROCESSED_KEY, usuario_id, "entregado")
            print(f"Mensaje reenviado a {usuario_id} por {canal}.")
            return
    print(f"No se pudo entregar el mensaje a {usuario_id} por ningún canal.")

asyncio.run(consume_messages())