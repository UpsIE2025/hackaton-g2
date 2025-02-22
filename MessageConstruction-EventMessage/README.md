# Historia Técnica

COMO un arquitecto de software,

QUIERO implementar un sistema de notificación de eventos basado en mensajería asíncrona,

PARA garantizar la entrega confiable de eventos entre aplicaciones sin acoplamiento directo.

# Criterios de Aceptación

DADO que un sujeto genera un evento,
CUANDO el evento es empaquetado en un mensaje y enviado por un canal de mensajería,
ENTONCES el mensaje debe ser publicado en una cola o tópico específico sin pérdida de datos.

DADO que el observador está suscrito al canal de mensajería,
CUANDO reciba un mensaje de evento,
ENTONCES deberá procesarlo correctamente y confirmar la recepción.

DADO que el mensaje de evento es enviado,
CUANDO el observador no esté disponible,
ENTONCES el sistema de mensajería deberá retener el mensaje hasta que el observador pueda procesarlo.

DADO un evento crítico,
CUANDO el observador no pueda procesar el mensaje en el primer intento,
ENTONCES el sistema deberá reintentarlo según una política de reintentos configurada.

## Ejemplo de la Vida Real

Imagina un sistema de pedidos en un e-commerce. Cuando un usuario realiza una compra, el sistema de órdenes (sujeto) genera un evento "Pedido Creado" y lo envía a un bus de eventos (Kafka, RabbitMQ, etc.). El sistema de facturación (observador) escucha estos eventos y, al recibir el mensaje, genera la factura correspondiente. Si el sistema de facturación está inactivo, el mensaje se almacena en la cola hasta que pueda procesarlo.

# Ejecutar y probar:

1. Correr los contenedores:
`
docker-compose up -d
`
2. Crear el entoro virtual e instalar requerimientos:
`
python -m venv env
`

    En Windows:
`env\Scripts\activate
`
    
    En Linux/Mac:
`
source env/bin/activate
`
3. Instalar requerimientos:
`
pip install -r requirements.txt
`
4. Ejecutar el consumidor:
`
python consumer.py
`
5. Ejecutar el productor:
`
python producer.py
`