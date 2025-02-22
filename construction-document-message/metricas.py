from fastapi import FastAPI, HTTPException
import uvicorn
from aiokafka import AIOKafkaConsumer
import redis
import json
import asyncio
# Configuración de Kafka y Redis
KAFKA_TOPIC = "js-construction-oferta"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PROCESSED_KEY = "mensajes_procesados"

# Cliente Redis
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)



def obtener_metricas():
    """
    Obtiene métricas de envíos, entregas y fallos.
    """
    total_mensajes = redis_client.hlen(REDIS_PROCESSED_KEY)
    entregados = sum(1 for estado in redis_client.hvals(REDIS_PROCESSED_KEY) if estado == "entregado")
    fallos = total_mensajes - entregados
    print(f"Total de mensajes: {total_mensajes}")
    print(f"Mensajes entregados: {entregados}")
    print(f"Mensajes con fallos: {fallos}")


# Ejecutar la aplicación FastAPI
if __name__ == "__main__":
   obtener_metricas()