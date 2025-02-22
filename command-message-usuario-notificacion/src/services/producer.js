
const { Kafka } = require('kafkajs');
const MessageCommand = require('../models/MessageCommand');

const kafka = new Kafka({
  clientId: 'messenger-notification-producer',
  brokers: ['localhost:9092']
});

const producer = kafka.producer();

async function sendMessageNotification(senderId, receiverId, content) {
  try {
    await producer.connect();
    
    // Crear comando de mensaje usando el patrón Command Message
    const command = new MessageCommand(senderId, receiverId, content);

    // Enviar comando al tópico de Kafka
    await producer.send({
      topic: 'pv-message-notifications',
      messages: [
        { 
          // Usar receiverId como key para particionamiento
          key: receiverId.toString(),
          value: JSON.stringify(command.toJSON())
        }
      ],
    });

    console.log(`Notification command sent for message ${command.messageId}`);
    return command.messageId;
  } catch (error) {
    console.error('Error sending notification:', error);
    throw error;
  }
}

module.exports = {
  sendMessageNotification
};