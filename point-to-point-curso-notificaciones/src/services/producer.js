const { Kafka } = require('kafkajs');
const { v4: uuidv4 } = require('uuid');

// Configuración del cliente Kafka
const kafka = new Kafka({
  clientId: 'course-notification-producer',
  brokers: ['localhost:9092']
});

const producer = kafka.producer();

// Función para enviar notificación de asignación de curso
async function sendCourseAssignment(studentId, courseId) {
  try {
    await producer.connect();
    
    // Crear mensaje con ID único
    const message = {
      messageId: uuidv4(),
      studentId,
      courseId,
      timestamp: new Date().toISOString()
    };

    // Enviar mensaje al tópico
    await producer.send({
      topic: 'course-assignments',
      messages: [
        { 
          key: studentId.toString(),
          value: JSON.stringify(message)
        }
      ],
    });

    console.log(`Mensaje enviado: ${JSON.stringify(message)}`);
    return message.messageId;
  } catch (error) {
    console.error('Error al enviar mensaje:', error);
    throw error;
  }
}

module.exports = { sendCourseAssignment };