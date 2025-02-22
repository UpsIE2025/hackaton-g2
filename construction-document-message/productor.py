from aiokafka import AIOKafkaProducer
import json
import asyncio


KAFKA_TOPIC = "js-construction-oferta"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"


to_bytes = lambda x: json.dumps(x).encode('utf-8')

async def enviar_oferta(usuario_id: str, mensaje: str, canal_prioritario: str):
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()


    oferta = {
        "usuario_id": usuario_id,
        "mensaje": mensaje,
        "canal_prioritario": canal_prioritario,
        "intentos": 0
    }


    await producer.send(KAFKA_TOPIC, to_bytes(oferta))
    print(f"Oferta enviada para el usuario {usuario_id}.")

    await producer.stop()


asyncio.run(enviar_oferta("1235", "¡Oferta especial para ti del 10%!", "sms"))