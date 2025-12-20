# Imagen base de Python
FROM python:3.9-slim

# Directorio de trabajo dentro del Docker.
WORKDIR /app

# Instalo las dependencias
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copio la aplicación
COPY  ["helloWorld.py", "config.cfg", "./"]
# Antes copio la config 
#COPY  helloWorld.py microservices.cfg ./

# Copio la config.
#COPY ../../configs/microservices.cfg

# Expone el puerto del Docker
EXPOSE 2202

# Comando para ejecutar la pp.
CMD ["python", "helloWorld.py"]
