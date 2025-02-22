**Historia Técnica: Manejo de Mensajes Inválidos en un Sistema de Mensajería**

### Contexto
Imagina que una empresa de logística gestiona un sistema de notificaciones para actualizar a los clientes sobre el estado de sus envíos. Este sistema recibe mensajes de diferentes fuentes, como sensores en almacenes, aplicaciones móviles de repartidores y sistemas de seguimiento de paquetes. Sin embargo, en ocasiones algunos mensajes llegan con datos incorrectos, mal formateados o sin la información necesaria para ser procesados. Para evitar que estos mensajes causen fallos en el sistema principal, es necesario un mecanismo para gestionar mensajes inválidos.

### Historia Técnica
#### **Título:** Manejo de Mensajes Inválidos en el Sistema de Notificaciones

**COMO** desarrollador del sistema de mensajería,  
**QUIERO** que los mensajes incorrectos sean movidos automáticamente a un canal especial de mensajes no válidos,  
**PARA** que el sistema pueda seguir operando sin interrupciones y los mensajes problemáticos puedan ser analizados posteriormente.

### **Criterios de Aceptación**
1. **Validación de Mensajes:**  
   - **DADO** un mensaje recibido,  
   - **CUANDO** su formato sea incorrecto o tenga datos faltantes,  
   - **ENTONCES** debe ser considerado inválido.

2. **Canal de Mensajes No Válidos:**  
   - **DADO** un sistema de mensajería,  
   - **CUANDO** se identifique un mensaje inválido,  
   - **ENTONCES** debe ser movido automáticamente a un canal de mensajes no válidos.

3. **Manejo de Mensajes Inválidos:**  
   - **DADO** un mensaje inválido detectado,  
   - **CUANDO** se mueva al canal correspondiente,  
   - **ENTONCES** debe registrarse un evento en los logs con detalles del mensaje y la razón del fallo.

4. **Revisión y Recuperación:**  
   - **DADO** un canal de mensajes no válidos,  
   - **CUANDO** un administrador acceda a estos mensajes,  
   - **ENTONCES** podrá analizarlos y, si es posible, corregir y reenviar el mensaje a su canal de destino original.


---


### **Criterios de Aceptación Cumplidos - Técnica**
1. En `consumer.js`, se valida si el mensaje tiene `userId` y `action`. Si falta algún dato, el mensaje se considera inválido y se guarda en Redis en la lista `invalid-events`.
2. Los eventos inválidos son movidos a Redis (`invalid-events`) para su posterior revisión.
3. En `consumer.js`, cuando se detecta un mensaje inválido, se imprime un log `console.log("⚠️ Evento inválido detectado:", event);` y se guarda en Redis.
4. En `api.js`, la ruta `/invalid-events` permite recuperar los mensajes inválidos almacenados en Redis, permitiendo su análisis y posible corrección.

---


### **Pasos para Compilar y Ejecutar**

1. **Clonar el repositorio:**
   ```sh
   git clone  https://github.com/UpsIE2025/hackaton-g2.git
   cd MessageChannel/InvalidMessage
   ```

2. **Iniciar los contenedores Docker:**
   ```sh
   docker-compose up -d
   ```

3. **Instalar dependencias en Node.js:**
   ```sh
   npm install
   ```

4. **Ejecutar el productor de Kafka:**
   ```sh
   node producer.js
   ```

5. **Ejecutar el consumidor de Kafka:**
   ```sh
   node consumer.js
   ```

6. **Ejecutar la API para consultar mensajes en Redis:**
   ```sh
   node api.js
   ```

7. **Verificar los mensajes en Redis:**
   - Abrir `http://localhost:8081` en un navegador para acceder a Redis Commander.

8. **Ver logs de Kafka:**
   ```sh
   docker logs kafka
   ```
