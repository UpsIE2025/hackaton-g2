# Historia de Usuario Técnica

COMO arquitecto de software,

QUIERO que el sistema utilice un canal de comunicación separado para cada tipo de datos,

PARA garantizar que los datos sean transmitidos y recibidos de manera organizada y sin ambigüedades.

# Criterios de Aceptación

DADO que un remitente necesita enviar datos, CUANDO determine el tipo de datos a enviar, ENTONCES deberá seleccionar el canal correspondiente.

DADO que el sistema reciba datos en un canal específico, CUANDO el receptor obtenga los datos de ese canal, ENTONCES deberá inferir correctamente su tipo sin necesidad de información adicional.

DADO un sistema con múltiples tipos de datos, CUANDO un tipo de datos desconocido quiera ser transmitido, ENTONCES deberá avisar que el tipo de datos es desconocido.


# Ejecutar y probar:

1. Correr los contenedores:
`
docker-compose up -d
`
2. Crear el entoro virtual e instalar requerimientos:
`
python -m venv env
`

    En Windows:
`env\Scripts\activate
`
    
    En Linux/Mac:
`
source env/bin/activate
`
3. Instalar requerimientos:
`
pip install -r requirements.txt
`
4. Ejecutar el consumidor:
`
python consumer.py
`
5. Ejecutar el productor:
`
python producer.py
`
