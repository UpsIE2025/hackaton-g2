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

  await consumer.subscribe({ topic: 'dc-user-events', fromBeginning: true });

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      const event = JSON.parse(message.value.toString());
      const { userId, action, productId } = event;

      console.log(`Evento recibido: ${action} de usuario ${userId} en el producto ${productId}`);

      const recommendations = generateRecommendations(userId, productId);

      await redis.set(`user:${userId}:recommendations`, JSON.stringify(recommendations), 'EX', 3600); 

      console.log(`Recomendaciones para usuario ${userId}:`, recommendations);

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

start().catch(console.error);
