PATRON CONSTRUCTION RETURN ADDRESS
* Descripcion
El mensaje de solicitud debe contener una dirección de devolución que indique dónde enviar el mensaje de respuesta.
De esta manera, el que responde no necesita saber a dónde enviar la respuesta.
Si diferentes mensajes para el responder requieren respuestas a diferentes lugares, el que responde sabe dónde enviar la respuesta para cada solicitud.
Esto encapsula el conocimiento de qué canales usar para solicitudes y respuestas dentro del solicitante, de modo que esas decisiones no tengan que estar codificadas en el que responde

* Historia de Usuario
COMO un desarrollador de sistemas de mensajería,
QUIERO que los mensajes de solicitud incluyan una dirección de devolución,
PARA que el sistema que responde pueda enviar la respuesta sin necesidad de conocer el destino previamente.

* Criterios de Aceptación
    * DADO un mensaje de solicitud, CUANDO este sea enviado, ENTONCES deberá contener una dirección de devolución para recibir la respuesta.
    * DADO un sistema que responde a solicitudes, CUANDO procese una solicitud, ENTONCES deberá enviar la respuesta a la dirección de devolución proporcionada en el mensaje original.
    * DADO múltiples solicitudes con diferentes direcciones de devolución, CUANDO el sistema que responde las procese, ENTONCES deberá enviar cada respuesta a su respectiva dirección de devolución.
    * DADO un sistema de mensajería, CUANDO un solicitante envíe una solicitud, ENTONCES deberá encapsular la información de los canales de solicitud y respuesta sin necesidad de que el que responde tenga este conocimiento codificado.


* Pre Requisitos
    Instalar docker desktop y docker compose
    Instalar node
    Instalar postman
* Ejecución
    * Clonar el repositorio en su maquina local
    * Ubicarse en la raiz del proyecto y ejecutar el comando docker compose up -d 
    * Navegar a la ruta /construction-return-address
    * Para el requester 1: Ejecutar el comando node requester1.js
        * Invocar el endpoint http://localhost:26061/publish con el metodo post y enviar en el body el siguiente json:
        { 
            "id": 111,
            "amount": 5000.00    
        }
    * Para el requester 2: Ejecutar el comando node requester2.js. 
        * Invocar el endpoint http://localhost:26062/publish con el metodo post y enviar en el body el siguiente json:
       { 
            "user": "Gio",
            "email": "gio@gmail.com"
        }
    * Para ejecutar el replier : Ejecutar el comando node replier.js