const { Kafka } = require('kafkajs');
const Redis = require('ioredis');

const kafka = new Kafka({
  clientId: 'messenger-notification-consumer',
  brokers: ['localhost:9092']
});

const redis = new Redis();
const consumer = kafka.consumer({ groupId: 'notification-service-group' });

const NOTIFICATION_LOCK_TIMEOUT = 60 * 1000; // 1 minuto

async function startConsumer() {
  try {
    await consumer.connect();
    await consumer.subscribe({ topic: 'pv-message-notifications', fromBeginning: true });

    await consumer.run({
      eachMessage: async ({ message }) => {
        const notification = JSON.parse(message.value.toString());
        const lockKey = `notification:${notification.messageId}`;
        
        try {
          // Intentar obtener un lock en Redis para evitar duplicados
          const acquired = await redis.set(
            lockKey,
            'processing',
            'PX',
            NOTIFICATION_LOCK_TIMEOUT,
            'NX'
          );

          if (acquired) {
            // Simulación de envío de notificación
            console.log(`🔔 Notificación enviada al usuario ${notification.receiverId}:`);
            console.log(`   De: Usuario ${notification.senderId}`);
            console.log(`   Mensaje: ${notification.content}`);
            
            // Registrar notificación como enviada
            await redis.set(
              `sent:${notification.messageId}`,
              JSON.stringify({
                status: 'delivered',
                timestamp: new Date().toISOString()
              })
            );

            // Liberar el lock
            await redis.del(lockKey);
          } else {
            console.log(`Notificación ${notification.messageId} ya procesada`);
          }
        } catch (error) {
          console.error(`Error al procesar la notificación ${notification.messageId}:`, error);
          // Asegurar que el lock se libere en caso de error
          await redis.del(lockKey);
        }
      },
    });

    console.log('Consumidor de notificaciones iniciado correctamente');
  } catch (error) {
    console.error('Error al iniciar el consumidor:', error);
    throw error;
  }
}

module.exports = { startConsumer };