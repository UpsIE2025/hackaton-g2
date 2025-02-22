from kafka import KafkaConsumer
import json

# Configuración de Kafka
consumer = KafkaConsumer('js-router-filter-message', bootstrap_servers='localhost:9092', value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# Función para procesar mensajes
def process_messages():
    for message in consumer:
        center_id = message.value['center_id']
        msg = message.value['message']
        print(f"Centro {center_id} procesando mensaje: {msg}")

# Ejemplo de uso
if __name__ == "__main__":
    process_messages()