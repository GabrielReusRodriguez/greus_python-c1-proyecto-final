# Imagen base de Python
FROM python:3.9-slim

# Directorio de trabajo dentro del Docker.
WORKDIR /app

# Instalo las dependencias
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copio la aplicación
RUN mkdir /app/recursos
COPY  ["run.py", "app.py", "config.cfg", "./"] 
COPY recursos/ /app/recursos  

# Expone el puerto del Docker
EXPOSE 2203

# Comando para ejecutar la app.
CMD ["python", "run.py"]
