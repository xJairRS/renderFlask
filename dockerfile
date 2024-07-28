# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo requirements.txt en el directorio de trabajo
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos de la aplicación en el contenedor
COPY . .

# Expone el puerto en el que correrá la aplicación Flask
EXPOSE 5000

# Define el comando para correr la aplicación
CMD ["python", "Server_TT.py"]
