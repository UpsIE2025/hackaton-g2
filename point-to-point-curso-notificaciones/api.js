const express = require('express');
const { sendCourseAssignment } = require('./src/services/producer');

const app = express();
app.use(express.json());

// Ruta única
app.post('/api/course-assignment', async (req, res) => {
  try {
    const { studentId, courseId } = req.body;
    
    if (!studentId || !courseId) {
      return res.status(400).json({ 
        error: 'studentId y courseId son requeridos' 
      });
    }

    const messageId = await sendCourseAssignment(studentId, courseId);
    
    res.json({ 
      success: true, 
      messageId,
      message: `Asignación enviada para estudiante ${studentId} en curso ${courseId}`
    });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ 
      error: 'Error al enviar la asignación del curso' 
    });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Servidor corriendo en http://localhost:${PORT}`);
});

// Inicializar consumidores
const { startConsumer } = require('./src/services/consumer');

// Iniciar 3 consumidores
for (let i = 1; i <= 3; i++) {
  startConsumer(`consumer-${i}`).catch(console.error);
}