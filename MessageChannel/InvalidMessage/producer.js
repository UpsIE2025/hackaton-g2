const { Kafka } = require("kafkajs");

const kafka = new Kafka({
  clientId: "marketing-producer",
  brokers: ["localhost:9092"],
});

const producer = kafka.producer();

const run = async () => {
  await producer.connect();
  
  setInterval(async () => {
    const event = {
      userId: Math.floor(Math.random() * 1000),
      action: Math.random() > 0.2 ? "click" : null, // Simula error en algunos casos
      timestamp: Date.now(),
    };

    await producer.send({
      topic: "dc-invalid-message",
      messages: [{ value: JSON.stringify(event) }],
    });

    console.log("📨 Evento enviado:", event);
  }, 3099);
};

run().catch(console.error);
