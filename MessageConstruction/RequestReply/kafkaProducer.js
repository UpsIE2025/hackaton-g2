const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'recomendation-service',
  brokers: ['localhost:9092'],
});

const producer = kafka.producer();

async function sendMessage() {
  try {
    const message = {
      userId: 123,     
      action: 'clicked', 
      productId: 'abc123' 
    };

    await producer.send({
      topic: 'dc-user-events',
      messages: [
        {
          value: JSON.stringify(message),
        },
      ],
    });

    console.log('Mensaje de solicitud enviado a Kafka');

    await getResponse();
  } catch (error) {
    console.error('Error enviando el mensaje:', error);
  }
}

async function getResponse() {
  const consumer = kafka.consumer({ groupId: 'request-reply-group' });

  await consumer.connect();
  await consumer.subscribe({ topic: 'dc-recomendations-topic' });

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      const response = JSON.parse(message.value.toString());
      console.log('Respuesta recibida:', response);

    },
  });
}

async function start() {
  try {
    await producer.connect();
    console.log("Conectado al productor de Kafka");

    await sendMessage();
  } catch (error) {
    console.error('Error al iniciar el productor de Kafka:', error);
  }
}

start().catch(console.error);
