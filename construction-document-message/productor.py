from aiokafka import AIOKafkaProducer
import json
import asyncio

# Configuración de Kafka
KAFKA_TOPIC = "js-construction-oferta"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"

# Función para serializar a bytes
to_bytes = lambda x: json.dumps(x).encode('utf-8')

async def enviar_oferta(usuario_id: str, mensaje: str, canal_prioritario: str):
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()

    # Crear el mensaje de documento
    oferta = {
        "usuario_id": usuario_id,
        "mensaje": mensaje,
        "canal_prioritario": canal_prioritario,
        "intentos": 0
    }

    # Enviar el mensaje a Kafka
    await producer.send(KAFKA_TOPIC, to_bytes(oferta))
    print(f"Oferta enviada para el usuario {usuario_id}.")

    await producer.stop()

# Ejemplo de uso
asyncio.run(enviar_oferta("1235445", "¡Oferta especial para ti del 10%!", "sms"))