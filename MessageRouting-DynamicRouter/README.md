# Historia Técnica:
COMO desarrollador de integración de sistemas,

QUIERO implementar un enrutador dinámico que pueda autoconfigurarse según los mensajes de configuración de los destinos participantes,

PARA asegurar una distribución eficiente de los mensajes a los destinatarios adecuados en función de sus reglas definidas.

# Criterios de Aceptación:

DADO que el enrutador dinámico está en operación, CUANDO un nuevo destinatario se registre enviando un mensaje especial al canal de control, ENTONCES el enrutador deberá almacenar sus reglas de preferencia en la base de reglas.

DADO que un mensaje es recibido por el enrutador dinámico, CUANDO las reglas almacenadas sean evaluadas, ENTONCES el mensaje deberá ser enviado solo al destinatario cuyas reglas coincidan con los criterios del mensaje.

DADO que un destinatario cambia sus condiciones de recepción, CUANDO envíe un nuevo mensaje de configuración al canal de control, ENTONCES el enrutador deberá actualizar la base de reglas para reflejar las nuevas condiciones.

DADO que un destinatario deja de estar disponible, CUANDO no envíe su mensaje de configuración en un periodo determinado, ENTONCES el enrutador deberá eliminar sus reglas de la base de datos para evitar intentos de enrutamiento incorrectos.

DADO que un mensaje no coincide con ninguna de las reglas almacenadas, CUANDO el enrutador evalúe las condiciones, ENTONCES el mensaje deberá ser rechazado o enviado a un destino por defecto.
