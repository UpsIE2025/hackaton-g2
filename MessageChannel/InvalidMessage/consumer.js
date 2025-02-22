const { Kafka } = require("kafkajs");
const Redis = require("ioredis");

const kafka = new Kafka({
  clientId: "marketing-consumer",
  brokers: ["localhost:9092"],
});

const redis = new Redis();

const consumer = kafka.consumer({ groupId: "marketing-group" });

const run = async () => {
  await consumer.connect();
  await consumer.subscribe({ topic: "dc-invalid-message", fromBeginning: true });

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      const event = JSON.parse(message.value.toString());

      if (!event.userId || !event.action) {
        console.log("⚠️ Evento inválido detectado:", event);
        await redis.lpush("invalid-events", JSON.stringify(event));
      } else {
        await redis.set(`event:${event.userId}`, JSON.stringify(event));
        console.log("✅ Evento válido procesado:", event);
      }
    },
  });
};

run().catch(console.error);
