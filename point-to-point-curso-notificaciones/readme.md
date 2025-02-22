Historia técnica: Message Channel / Point to Point

La historia técnica implementada es la siguiente: COMO sistema de gestión de cursos en línea, QUIERO enviar notificaciones de asignación de curso a un solo usuario receptor, PARA asegurarme de que cada estudiante reciba la notificación de manera exclusiva y evitar duplicidades en la entrega. 

1. Flujo del Proceso
Envío del Mensaje:

* El cliente hace una petición POST con studentId y courseId
* El producer genera un ID único para el mensaje
* El mensaje se envía al tópico 'course-assignments' en Kafka

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