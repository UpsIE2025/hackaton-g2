from kafka import KafkaProducer
import json

# Configuración de Kafka
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Función para anunciar preferencias
def announce_preferences(center_id, preferences):
    producer.send('js-router-filter-control', value={'center_id': center_id, 'preferences': preferences})
    print(f"Preferencias anunciadas por {center_id}: {preferences}")

# Ejemplo de uso
if __name__ == "__main__":
    announce_preferences('center_a', {'accepts_urgent': True, 'accepts_heavy': False})
    announce_preferences('center_b', {'accepts_urgent': False, 'accepts_heavy': True})
   