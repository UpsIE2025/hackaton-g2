const express = require('express');
const { sendMessageNotification } = require('./services/producer');

const app = express();
app.use(express.json());

app.post('/api/messages', async (req, res) => {
  try {
    const { senderId, receiverId, content } = req.body;
    
    if (!senderId || !receiverId || !content) {
      return res.status(400).json({ 
        error: 'senderId, receiverId and content are required' 
      });
    }

    const messageId = await sendMessageNotification(senderId, receiverId, content);
    
    res.json({ 
      success: true, 
      messageId,
      message: `Message notification queued for delivery to user ${receiverId}`
    });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ 
      error: 'Error processing message notification' 
    });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});