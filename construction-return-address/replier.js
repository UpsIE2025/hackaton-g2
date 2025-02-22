const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'message-system',
  brokers: ['localhost:9092'] // Ajusta según tu configuración de Kafka
});

const producer = kafka.producer();
const consumer = kafka.consumer({ groupId: 'message-group' });
const topicRequestMessage = 'gj-request';

async function sendMessage(topic, message) {
  await producer.connect();
  await producer.send({
    topic,
    messages: [{ value: JSON.stringify(message) }]
  });
  await producer.disconnect();
}

// Escucha el topico gj-request;
async function processMessages() {
  await consumer.connect();
  await consumer.subscribe({ topic: topicRequestMessage, fromBeginning: true });

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      try {
        const msg = await JSON.parse(message.value.toString());
        const topicResponse = await msg.response
        console.log(`Se proceso el mensaje:`, msg);         

        await sendMessage(topicResponse, {content: `Solicitud procesada con éxito`})
        await heartbeat()
        console.log(`Respuesta publicada con exito:`, msg);         

      } catch (error) {
        console.error(`Error procesando mensaje: ${error.message}`);        
      }
    }
  });
}


// Iniciar el consumidor
processMessages().catch(console.error);
