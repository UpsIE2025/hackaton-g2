# Caso de Implementación: Sistema de Notificaciones para Ofertas Personalizadas con Kafka y Redis


Una empresa de comercio electrónico quiere mejorar su estrategia de marketing enviando ofertas personalizadas a sus clientes 
en función de su comportamiento de compra. Para ello,
 implementa un sistema basado en el patrón publish/subscribe con Apache Kafka y Redis, 
 asegurando que cada cliente reciba solo las ofertas que le corresponden y sin duplicaciones.





# Proyecto FastAPI con Kafka y Redis

Este proyecto es una aplicación web construida con **FastAPI** que interactúa con **Kafka** para el manejo de mensajes y **Redis** para almacenar los datos de ofertas de usuarios en tiempo real.

## Requisitos

- Python 3.8 o superior
- Docker (para ejecutar Kafka y Redis)
- **FastAPI**, **Uvicorn**, **aiokafka** y **redis-py**

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