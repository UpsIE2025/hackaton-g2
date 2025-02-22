from kafka import KafkaProducer
import json

# Configurar el productor
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Definir tipos de datos y sus canales
data_channels = {
    "usuario": "pr-channel-datatype-usuarios",
    "producto": "pr-channel-datatype-productos",
    "transaccion": "pr-channel-datatype-transacciones"
}

def send_data(data_type, data):
    """Envía datos al canal correspondiente en Kafka."""
    if data_type in data_channels:
        topic = data_channels[data_type]
        producer.send(topic, data)
        print(f"Datos enviados a {topic}: {data}")
    else:
        print(f"Tipo de datos desconocido: {data_type}")

# Ejemplo de envío
send_data("usuario", {"id": 1, "nombre": "Alice"})
send_data("producto", {"id": 101, "nombre": "Laptop"})
send_data("transaccion", {"id": 5001, "monto": 250.75})

# Cerrar el productor
producer.flush()
producer.close()
