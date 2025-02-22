const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'recomendation-service',
  brokers: ['localhost:9092'],
});

const producer = kafka.producer();

// Enviar mensaje al tema 'dc-user-events' y esperar respuesta
async function sendMessage() {
  try {
    const message = {
      userId: 123,     
      action: 'clicked', 
      productId: 'abc123' 
    };

    // Enviar el mensaje al tema 'dc-user-events' (Solicitud)
    await producer.send({
      topic: 'dc-user-events',
      messages: [
        {
          value: JSON.stringify(message),
        },
      ],
    });

    console.log('Mensaje de solicitud enviado a Kafka');

    // Esperar la respuesta en el tema 'recomendations-response'
    await getResponse();
  } catch (error) {
    console.error('Error enviando el mensaje:', error);
  }
}

// Esperar la respuesta del tema 'recomendations-response'
async function getResponse() {
  const consumer = kafka.consumer({ groupId: 'request-reply-group' });

  await consumer.connect();
  await consumer.subscribe({ topic: 'dc-recomendations-topic' });

  // Esperar y obtener la respuesta
  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      const response = JSON.parse(message.value.toString());
      console.log('Respuesta recibida:', response);

    },
  });
}

async function start() {
  try {
    // Conectar el productor de Kafka
    await producer.connect();
    console.log("Conectado al productor de Kafka");

    // Llamar a la función para enviar un mensaje
    await sendMessage();
  } catch (error) {
    console.error('Error al iniciar el productor de Kafka:', error);
  }
}

start().catch(console.error);
