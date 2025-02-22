# Sistema de Recomendaciones Personalizadas

Este sistema tiene como objetivo proporcionar recomendaciones personalizadas para los usuarios de un comercio en línea. Utiliza **Kafka** para la mensajería asíncrona entre el servicio productor (generador de recomendaciones) y el consumidor (procesador de interacciones de usuario), y **Redis** para almacenar las recomendaciones de manera eficiente.

## Contexto

En un sistema de recomendaciones personalizadas para un comercio en línea, los usuarios interactúan con productos realizando acciones como "ver un producto", "agregar al carrito" o "comprar". El sistema necesita generar recomendaciones basadas en estas interacciones, mejorando así la experiencia de compra del usuario.

## Historia Técnica

### **Como un usuario registrado**  
**Quiero** recibir recomendaciones personalizadas basadas en mi interacción con productos,  
**Para** mejorar mi experiencia de compra y encontrar productos que puedan interesarme.

### Criterios de Aceptación

#### Historia 1: Enviar solicitud de recomendación (Productor)

**DADO** que un usuario interactúa con un producto (como hacer clic en un producto) en la aplicación,  
**CUANDO** el sistema envía un mensaje con la información del usuario, acción y producto al tema `dc-user-events` de Kafka,  
**ENTONCES** el mensaje debe ser recibido correctamente por el consumidor de Kafka para generar las recomendaciones y responder al usuario.

#### Historia 2: Procesar solicitud de recomendación y generar respuesta (Consumidor)

**DADO** que un mensaje válido es recibido en el tema `dc-user-events`,  
**CUANDO** el consumidor procesa el mensaje,  
**ENTONCES** el consumidor debe generar recomendaciones para el usuario y almacenarlas en Redis con una expiración de una hora.

#### Historia 3: Enviar respuesta con recomendaciones (Consumidor)

**DADO** que el consumidor ha generado las recomendaciones,  
**CUANDO** el consumidor envía la respuesta con las recomendaciones al tema `dc-recomendations-topic` de Kafka,  
**ENTONCES** el productor debe recibir el mensaje con las recomendaciones y mostrarlas al usuario.

#### Historia 4: Almacenar recomendaciones en Redis

**DADO** que el consumidor genera recomendaciones para un usuario,  
**CUANDO** el sistema almacena las recomendaciones en Redis,  
**ENTONCES** las recomendaciones deben ser almacenadas con la clave `user:{userId}:recommendations` 
## Arquitectura

La solución se basa en una arquitectura desacoplada donde:

- **Kafka** actúa como intermediario de mensajes entre los distintos componentes (Productor y Consumidor).
- **Redis** se utiliza como almacenamiento en memoria para las recomendaciones, garantizando acceso rápido y eficiente.
- **Productor**: Envía los eventos de usuario al tema `dc-user-events` de Kafka.
- **Consumidor**: Recibe los eventos del tema `dc-user-events`, genera las recomendaciones personalizadas y las almacena en 

---

## Instalación y compilación
#### 1.Clonar el repositorio 
```sh
   git clone  https://github.com/UpsIE2025/hackaton-g2.git
   cd MessageConstruction/RequestReply
   ```
#### 2.Instalar las dependencias
```sh
   npm install kafkajs ioredis
   ```
#### 3. Ejecutar el Productor 
```sh
   node kafkaProducer.js
   ```
   
#### 4. Ejecutar el Consumidor 
```sh
   node kafkaConsumer.js
   ```

## Flujo de ejecución
- El Productor (kafkaProducer.js) enviará un mensaje con la información del usuario y su acción (por ejemplo, ver un producto) al tema user-events.
- El Consumidor (kafkaConsumer.js) escuchará el tema user-events, procesará el mensaje, generará las recomendaciones, las almacenará en Redis y las enviará al tema recomendations-response.
- El Productor puede luego recibir las recomendaciones desde el tema recomendations-response y procesarlas según lo necesite
