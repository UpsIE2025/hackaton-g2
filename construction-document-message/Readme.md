## Contexto
Imagina que trabajas en una empresa de comercio electrónico que envía ofertas personalizadas a sus clientes.
 Estas ofertas pueden ser enviadas a través de diferentes canales: Email, SMS o WhatsApp. 
 El sistema debe ser confiable, escalable y permitir que las ofertas se procesen de manera asíncrona.




Historia Técnica
COMO un arquitecto de software en marketing digital,
QUIERO implementar un sistema de notificaciones basado en Kafka y Redis,
PARA garantizar que cada cliente reciba una promoción única a través del mejor canal disponible.
Criterios de Aceptación
### 1. Entrega Única del Mensaje
DADO que un mensaje de promoción se publica en Kafka,
CUANDO múltiples consumidores intentan procesarlo,
ENTONCES solo un consumidor debe recibir y manejar ese mensaje.

### 2. Registro y Control de Entrega con Redis
DADO que un mensaje es recibido por un consumidor,
CUANDO se verifica el ID del cliente en Redis,
ENTONCES si el mensaje ya fue procesado, se descarta; si no, se marca como entregado.

### 3. Selección del Canal Adecuado
DADO que un cliente tiene múltiples canales disponibles (Email, SMS, WhatsApp),
CUANDO un mensaje es procesado,
ENTONCES el sistema debe seleccionar el canal prioritario basado en reglas de negocio.

### 4. Reintento en Caso de Falla
DADO que un mensaje fue enviado a un canal,
CUANDO no se recibe confirmación de entrega en X tiempo,
ENTONCES el mensaje se reenvía por otro canal disponible.

### 5. Monitoreo y Reporte
DADO que la campaña está en ejecución,
CUANDO se procesan mensajes,
ENTONCES el sistema debe generar métricas de envíos, entregas y fallos en un dashboard.




## Instalación

### 1. Clonar el repositorio

Primero, clona el repositorio en tu máquina local:

```bash
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio
### 2. Crear un entorno virtual (opcional -recomendado)
python -m venv venv
source venv/bin/activate  # En Windows usa `venv\Scripts\activate`

### 3. Instalar dependencias
pip install -r requirements.txt

### 4. Ejecutar el docker compose
docker-compose up

### 4. EJECUTAR 
uvicorn main:app --reload