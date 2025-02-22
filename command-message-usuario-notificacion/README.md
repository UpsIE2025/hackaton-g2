Historia técnica: Command Message

- Historia de Usuario Técnica
COMO sistema de mensajería red social,
QUIERO enviar notificaciones automáticas a los usuarios cuando reciban un nuevo mensaje,
PARA asegurarme de que cada usuario sea informado de manera confiable al recibir nuevos mensajes.

- Criterios de Aceptación
DADO que un usuario ha recibido un nuevo mensaje,
CUANDO se genere la notificación de mensaje,
ENTONCES se debe construir un comando que contenga los datos del mensaje y enviarlo al servicio de notificaciones.

DADO que el comando de notificación ha sido enviado,
CUANDO el servicio de notificaciones lo reciba,
ENTONCES debe procesar el comando e invocar el procedimiento para mostrar la notificación al usuario.

DADO que el mensaje se ha entregado con éxito,
CUANDO el usuario visualice la notificación,
ENTONCES el sistema debe marcar el mensaje como "notificado" para evitar duplicados.

Esta implementación sigue el patrón Command Message resumidas a continuación:

1. Flujo del Proceso

Envío del Mensaje:

* El cliente hace una petición POST con senderId, receiverId y content
* El producer genera un ID único para el mensaje
* El mensaje se envía al tópico 'pv-message-notifications' en Kafka


2. MessageCommand (Patrón Command Message):

* Encapsula toda la información necesaria para la notificación
* Garantiza que el mensaje sea autocontenido y serializable
* Incluye metadatos importantes como messageId y timestamp


3. Producer:

* Construye y envía comandos de notificación a Kafka
* Usa el receiverId como key para garantizar ordenamiento por receptor
* Maneja conexiones y errores apropiadamente

4. Consumer:

* Procesa los comandos de notificación de forma asíncrona
* Implementa un mecanismo de lock con Redis para evitar duplicados
* Simula el envío de notificaciones y registra su estado

5. Manejo de Duplicados:

* Usa Redis para implementar un sistema de locks distribuidos
* Mantiene registro de notificaciones enviadas
* Incluye timeout para evitar deadlocks

6. Cómo Probar en Insomnia

* Configurar Nueva Solicitud:
* Solicitud HTTP
* Método: POST
* URL: http://localhost:3000/api/messages

Configurar el Body:
json{
  "senderId": 1001,
  "receiverId": 1002,
  "content": "Hola, ¿cómo estás?"
}

Enviar y Observar:
Envía la solicitud
Debería recibir una respuesta como:
json{
  "success": true, 
  "messageId": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Notificación enviada para usuario 1002"
}

7. Verificar los Logs:

* En la terminal donde se ejecuta node api.js se verá:

* El mensaje siendo enviado
* El comando de notificación siendo construido
* El comando siendo enviado a Kafka
* El consumidor recibiendo y procesando el comando

Resumen flujo:
participant C as Cliente
    participant A as API
    participant P as Producer
    participant K as Kafka
    participant Con as Consumer
    participant R as Redis

    C->>A: POST /api/messages
    A->>P: sendMessageNotification()
    P->>K: Envía comando
    K-->>Con: Consume mensaje
    Con->>R: Intenta obtener lock
    R-->>Con: Otorga/Rechaza lock
    Con->>Con: Procesa notificación
    Con->>R: Guarda estado
    A-->>C: Respuesta con messageId