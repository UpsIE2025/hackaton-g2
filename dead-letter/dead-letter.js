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
const failedMessagesTopic = 'gj-failed-messages';

async function sendMessage(topic, message) {
  await producer.connect();
  await producer.send({
    topic,
    messages: [{ value: JSON.stringify(message) }]
  });
  await producer.disconnect();
}

async function processMessages() {
  await consumer.connect();
  await consumer.subscribe({ topic: failedMessagesTopic, fromBeginning: true });

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      try {
        const msg = JSON.parse(message.value.toString());
        console.log(`Se inicia el reproceso del mensaje:`, msg);                
      } catch (error) {
        console.error(`Error procesando mensaje: ${error.message}`);        
      }
    }
  });
}


// Enviar el mensaje con la siguiente estructura { content: message, fail: true o false }
app.post("/get-request", async (req, res) => {  
  const  data  = req.body;
  
  try {    
    let responseMessage = {}
    if (data.fail) {
      console.error ("La solicitud no pudo ser procesada. Se reintentará mas tarde!")
      responseMessage = { success: true, message: 'Mensaje publicado correctamente' }
      responseMessage = "La solicitud no pudo ser procesada se realizará el reintento mas tarde!"
      await sendMessage('messages', data);
    } else {
      responseMessage = { success: false, message: "La solicitud ha sido procesada exitosamente...!"}
      console.log ("La solicitud ha sido procesada exitosamente...!")
    }
    
    res.status(200).json(responseMessage);
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

app.listen(26061, () => {
  console.log('Servidor corriendo en el puerto 26061');
});

// Iniciar el consumidor
processMessages().catch(console.error);
