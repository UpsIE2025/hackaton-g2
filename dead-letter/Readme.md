PATRON DEAD LETTER

* Descripción
Cuando un sistema de mensajería determina que no puede o no debe entregar un mensaje, puede optar por mover el mensaje a un canal de mensajes fallidos.
La forma específica en que funciona un canal de mensajes fallidos depende de la implementación del sistema de mensajería.
Por lo general, cada máquina tiene su propio canal de mensajes fallidos local, de modo que se puede mover de una cola local a otra sin cualquier incertidumbre de la red.
Cuando de muere suele registrar la máquina y el canal en el que fallo.


* Historia de Usuario
    * COMO un administrador de sistemas de mensajería,
    * QUIERO que los mensajes que no puedan ser entregados sean movidos a un canal de mensajes fallidos,
    * PARA poder analizarlos y tomar acciones correctivas sin perder información.

    * Criterios de Aceptación
            * DADO que un mensaje no puede ser entregado, CUANDO el sistema de mensajería lo detecte, ENTONCES deberá moverlo automáticamente a un canal de mensajes fallidos.
            * DADO un mensaje en un canal de mensajes fallidos, CUANDO se registre el fallo, ENTONCES deberá almacenar la información de la máquina y el canal donde ocurrió el error.            
            * DADO un mensaje en el canal de mensajes fallidos, CUANDO un administrador lo revise, ENTONCES deberá poder acceder a los detalles del fallo para su análisis.
* Pre Requisitos
    Instalar docker desktop y docker compose
    Instalar node
    Instalar postman
* Ejecución
    * Clonar el repositorio en su maquina local
    * Ubicarse en la raiz del proyecto y ejecutar el comando docker compose up -d 
    * Navegar a la ruta /dead-letter
    * Ejecutar el comando node dead-letter.js
    * Invocar el endpoint http://localhost:26061/get-request con el metodo post y enviar en el body el siguiente json:
    { 
        "content": {
            "id": 1,
            "amount": 5000.00
        }, 
        "fail": false
    }
        * Con el campo "fail": false simulamos si el request fue  procesado correctamente (visualizar logs)
        * Con el campo "fail": true simulamos que el request no fue procesado correctamente, fue enviado al topico gj-failed-messages y nuestro consumer lo tomará y lo reprocesará (observar consola)