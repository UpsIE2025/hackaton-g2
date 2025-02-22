const express = require("express");
const Redis = require("ioredis");

const app = express();
const redis = new Redis();
const PORT = 3099;

app.get("/metrics/:userId", async (req, res) => {
  const { userId } = req.params;
  const data = await redis.get(`event:${userId}`);
  if (data) {
    res.json(JSON.parse(data));
  } else {
    res.status(404).json({ error: "No hay datos para este usuario." });
  }
});

app.get("/invalid-events", async (req, res) => {
  const events = await redis.lrange("invalid-events", 0, -1);
  res.json(events.map(JSON.parse));
});

app.listen(PORT, () => console.log(`🚀 API corriendo en http://localhost:${PORT}`));
