const { Kafka } = require('kafkajs');
const Redis = require('ioredis');

// Configuración de Kafka
const kafka = new Kafka({
  clientId: 'course-notification-consumer',
  brokers: ['localhost:9092']
});

// Configuración de Redis
const redis = new Redis();

// Tiempo de expiración del lock en Redis (5 segundos)
const LOCK_TIMEOUT = 5000;

async function startConsumer(consumerId) {
  try {
    const consumer = kafka.consumer({ groupId: 'course-notification-group' });
    
    await consumer.connect();
    await consumer.subscribe({ topic: 'course-assignments', fromBeginning: true });

    await consumer.run({
      eachMessage: async ({ message }) => {
        const messageData = JSON.parse(message.value.toString());
        const lockKey = `lock:${messageData.messageId}`;
        
        try {
          // Intentar obtener lock exclusivo en Redis
          const acquired = await redis.set(
            lockKey,
            consumerId,
            'PX',
            LOCK_TIMEOUT,
            'NX'
          );

          if (acquired) {
            // Procesar el mensaje si obtuvimos el lock
            await processMessage(messageData);
            
            // Eliminar el lock después de procesar
            await redis.del(lockKey);
            
            console.log(`Consumidor ${consumerId} procesó mensaje ${messageData.messageId}`);
          } else {
            console.log(`Consumidor ${consumerId} ignoró mensaje ${messageData.messageId} (ya bloqueado)`);
          }
        } catch (error) {
          console.error(`Error procesando mensaje ${messageData.messageId}:`, error);
          // Asegurar que el lock se libere en caso de error
          await redis.del(lockKey);
        }
      },
    });

    console.log(`Consumidor ${consumerId} iniciado y escuchando mensajes...`);
  } catch (error) {
    console.error('Error en consumidor:', error);
    throw error;
  }
}

// Función que simula el procesamiento real del mensaje
async function processMessage(messageData) {
  // Simular algún procesamiento
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  console.log(`Notificación enviada al estudiante ${messageData.studentId} ` +
              `para el curso ${messageData.courseId}`);
}

module.exports = { startConsumer };