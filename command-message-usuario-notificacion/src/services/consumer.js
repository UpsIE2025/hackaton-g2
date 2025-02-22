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
            // Simular envío de notificación
            console.log(`🔔 Notification sent to user ${notification.receiverId}:`);
            console.log(`   From: User ${notification.senderId}`);
            console.log(`   Message: ${notification.content}`);
            
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
            console.log(`Notification ${notification.messageId} already processed`);
          }
        } catch (error) {
          console.error(`Error processing notification ${notification.messageId}:`, error);
          // Asegurar que el lock se libere en caso de error
          await redis.del(lockKey);
        }
      },
    });

    console.log('Notification consumer started successfully');
  } catch (error) {
    console.error('Error starting consumer:', error);
    throw error;
  }
}