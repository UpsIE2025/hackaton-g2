const { Kafka } = require('kafkajs');
const Redis = require('ioredis');

const kafka = new Kafka({
  clientId: 'recomendation-service',
  brokers: ['localhost:9092'],
});

const consumer = kafka.consumer({ groupId: 'recomendation-group' });
const producer = kafka.producer();

const redis = new Redis({
  host: 'localhost',
  port: 6379,
});

function generateRecommendations(userId, productId) {
  return [`Producto relacionado con ${productId}`, `Producto similar a ${productId}`];
}

async function start() {
  
  await producer.connect();
  console.log("Conectado al productor de Kafka");

  await consumer.connect();
  console.log("Conectado al consumidor de Kafka");

  // Suscripción al tema de eventos de usuario
  await consumer.subscribe({ topic: 'dc-user-events', fromBeginning: true });

  // Consumir los mensajes del tema 'dc-user-events'
  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      const event = JSON.parse(message.value.toString());
      const { userId, action, productId } = event;

      console.log(`Evento recibido: ${action} de usuario ${userId} en el producto ${productId}`);

      // Generar recomendaciones para el usuario
      const recommendations = generateRecommendations(userId, productId);

      // Almacenar las recomendaciones en Redis
      await redis.set(`user:${userId}:recommendations`, JSON.stringify(recommendations), 'EX', 3600); // Expira en 1 hora

      console.log(`Recomendaciones para usuario ${userId}:`, recommendations);

      // Enviar mensaje con las recomendaciones a un tema de Kafka (por ejemplo, 'dc-recomendations-topic')
      await producer.send({
        topic: 'dc-recomendations-topic',
        messages: [
          {
            value: JSON.stringify({
              userId,
              recommendations,
            }),
          },
        ],
      });

      console.log(`Recomendaciones enviadas para el usuario ${userId}`);
    },
  });
}

// Iniciar el servicio
start().catch(console.error);
