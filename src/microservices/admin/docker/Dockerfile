# Imagen base de Python
FROM python:3.9-slim

# Directorio de trabajo dentro del Docker.
WORKDIR /app

ARG ADMIN_PORT

# Instalo las dependencias
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copio la aplicación
COPY  ["run.py", "app.py", "db.py", "./"] 
COPY modules/ /app/modules

# Expone el puerto del Docker
#EXPOSE 2204
EXPOSE $ADMIN_PORT

# Comando para ejecutar la app.
CMD ["python", "run.py"]
