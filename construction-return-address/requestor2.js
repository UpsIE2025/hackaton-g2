const { Kafka } = require('kafkajs');
const express = require('express');
const app = express();

app.use(express.json());

const kafka = new Kafka({
  clientId: 'message-system',
  brokers: ['localhost:9092'] // Ajusta según tu configuración de Kafka
});

const producer = kafka.producer();
const consumer = kafka.consumer({ groupId: 'message-group' });
const topicResponseMessage = 'gj-reply2';
const topicRequestMessage = 'gj-request';

async function sendMessage(topic, message) {
  await producer.connect();
  await producer.send({
    topic,
    messages: [{ value: JSON.stringify(message) }]
  });
  await producer.disconnect();
}

// Escucha el topico gj-reply2
async function processMessages() {
  await consumer.connect();
  await consumer.subscribe({ topic: topicResponseMessage, fromBeginning: true });

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      try {
        const msg = await JSON.parse(message.value.toString());
        console.log(`Respuesta recibida en el requester 2:`, msg);   
        await heartbeat()             
      } catch (error) {
        console.error(`Error procesando mensaje: ${error.message}`);        
      }
    }
  });
}


// Enviar el mensaje con la siguiente estructura { content: message, response: gj-reply2 }
app.post("/publish", async (req, res) => {  
  const  data  = {
    "content": req.body,
    "response": topicResponseMessage
  }
  
  try {        
    await sendMessage(topicRequestMessage, data);     
    
    res.status(200).json({ success: true, message: "Requester 2 - Mensaje publicado exitosamente...!"});
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

app.listen(26062, () => {
  console.log('Servidor corriendo en el puerto 26062');
});

// Iniciar el consumidor
processMessages().catch(console.error);
