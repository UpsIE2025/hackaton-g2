const express = require('express');
const { sendMessageNotification } = require('./services/producer');

const app = express();
app.use(express.json());

app.post('/api/messages', async (req, res) => {
  try {
    const { senderId, receiverId, content } = req.body;
    
    // Valida los datos
    if (!senderId || !receiverId || !content) {
      return res.status(400).json({ 
        error: 'senderId, receiverId and content are required' 
      });
    }

    // Llama al producer
    const messageId = await sendMessageNotification(senderId, receiverId, content);
    
    res.json({ 
      success: true, 
      messageId,
      message: `Notificación de mensaje en cola para su entrega al usuario ${receiverId}`
    });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ 
      error: 'Error al procesar la notificación de mensaje' 
    });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Servidor corriendo en http://localhost:${PORT}`);
});