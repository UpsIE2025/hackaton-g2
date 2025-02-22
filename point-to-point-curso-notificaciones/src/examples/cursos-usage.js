// src/examples/cursos-usage.js
const producer = require('../services/producer');
const consumer = require('../services/consumer');

async function runExample() {
  // Iniciar 3 consumidores
  for (let i = 1; i <= 3; i++) {
    consumer.startConsumer(`consumer-${i}`);
  }

  // Datos de prueba
  const students = [1001, 1002, 1003];
  const courses = [101, 102, 103];

  // Enviar mensajes de prueba
  for (const studentId of students) {
    for (const courseId of courses) {
      await producer.sendCourseAssignment(studentId, courseId);
      // Esperar un poco entre mensajes
      await new Promise(resolve => setTimeout(resolve, 500));
    }
  }
}

// Si ejecutamos este archivo directamente
if (require.main === module) {
  console.log('Iniciando ejemplo de uso...');
  runExample().catch(console.error);
}

module.exports = { runExample };