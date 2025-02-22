const producer = require('../services/producer');
const consumer = require('../services/consumer');

async function runExample() {
  // Iniciar el consumidor
  await consumer.startConsumer();

  // Simular algunos mensajes de ejemplo
  const messages = [
    { from: 1001, to: 2001, content: "¡Hola! ¿Cómo estás?" },
    { from: 2001, to: 1001, content: "¡Bien! ¿Y tú?" },
    { from: 1001, to: 2001, content: "Todo excelente, gracias" }
  ];

  // Enviar mensajes con un pequeño delay entre ellos
  for (const msg of messages) {
    await producer.sendMessageNotification(msg.from, msg.to, msg.content);
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
}

// Si ejecutamos este archivo directamente
if (require.main === module) {
  console.log('Starting Messenger example...');
  runExample().catch(console.error);
}