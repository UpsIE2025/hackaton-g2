from kafka import KafkaConsumer, KafkaProducer
import redis
import json
from threading import Thread


producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
redis_client = redis.Redis(host='localhost', port=6379, db=0)


def receive_preferences():
    consumer = KafkaConsumer(
        'js-router-filter-control',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_offset_reset='earliest'  
    )
    print("Escuchando preferencias en control_channel...") 
    for message in consumer:
        center_id = message.value['center_id']
        preferences = message.value['preferences']
        # Almacena las preferencias en Redis
        redis_client.hset('routing_rules', center_id, json.dumps(preferences))
        print(f"Preferencias recibidas de {center_id}: {preferences}")

# Función para enrutar mensajes
def route_message(message):
    centers = redis_client.hgetall('routing_rules')
    for center_id, prefs_json in centers.items():
        preferences = json.loads(prefs_json)
        if evaluate_rules(message, preferences):
            producer.send('message_channel', value={'center_id': center_id.decode('utf-8'), 'message': message})
            print(f"Mensaje enviado a {center_id.decode('utf-8')}: {message}")
            break

# Función para evaluar reglas
def evaluate_rules(message, preferences):
    if message['type'] == 'urgent' and preferences.get('accepts_urgent'):
        return True
    if message['weight'] > 10 and preferences.get('accepts_heavy'):
        return True
    return False


def start_preference_listener():
    preference_thread = Thread(target=receive_preferences)
    preference_thread.daemon = True 
    preference_thread.start()

# Ejemplo de uso
if __name__ == "__main__":
    start_preference_listener()  

    # Simular un mensaje para enrutar
    message = {'type': 'urgent', 'weight': 5, 'destination': 'international'}
    route_message(message)