Historia técnica: Message Channel / Point to Point

- Historia de Usuario Técnica:
COMO sistema de gestión de cursos en línea,
QUIERO enviar notificaciones de asignación de curso a un solo usuario receptor,
PARA asegurarme de que cada estudiante reciba la notificación de manera exclusiva y evitar duplicidades en la entrega.

- Criterios de Aceptación:
DADO que un curso nuevo ha sido asignado a varios usuarios,
CUANDO se envíe la notificación a través del canal punto a punto,
ENTONCES solo un usuario recibirá cada mensaje individual de asignación.

DADO que hay varios usuarios inscritos y disponibles para recibir notificaciones,
CUANDO varios usuarios intenten recibir el mismo mensaje simultáneamente,
ENTONCES el canal garantizará que solo uno de ellos consuma con éxito ese mensaje.

DADO que hay múltiples mensajes de asignación de cursos pendientes,
CUANDO los usuarios estén disponibles para recibir mensajes,
ENTONCES cada usuario recibirá un mensaje único hasta que todos los mensajes sean consumidos.

1. Flujo del Proceso
Envío del Mensaje:

* El cliente hace una petición POST con studentId y courseId
* El producer genera un ID único para el mensaje
* El mensaje se envía al tópico 'pv-course-assignments' en Kafka

2. Consumo del Mensaje:

* Los tres consumidores están escuchando el tópico
* Cuando llega un mensaje, cada consumidor intenta obtener un lock en Redis
* Solo un consumidor obtiene el lock y procesa el mensaje
* Los otros consumidores ven que el lock existe y saltan el mensaje


3. Control de Concurrencia:

* Redis actúa como coordinador usando locks
* El lock expira después de 5 segundos (LOCK_TIMEOUT)
* Si un consumidor falla, el lock se libera automáticamente

4. Cómo Probar en Insomnia

* Configurar Nueva Solicitud:
* Solicitud HTTP
* Método: POST
* URL: http://localhost:3000/api/course-assignment

Configurar el Body:
json{
  "studentId": 1001,
  "courseId": 101
}

Enviar y Observar:
Envía la solicitud
Debería recibir una respuesta como:
json{
  "success": true,
  "messageId": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Asignación enviada para estudiante 1001 en curso 101"
}

5. Verificar los Logs:
En la terminal donde se ejecuta node api.js se verá:

* El mensaje siendo enviado
* Un consumidor adquiriendo el lock
* El mensaje siendo procesado
* El lock siendo liberado