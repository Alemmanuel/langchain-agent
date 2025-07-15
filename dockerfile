# Usa una imagen base ligera de Python
FROM python:3.10-slim-buster

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requisitos del backend e instala las dependencias
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos los archivos del backend al directorio de trabajo
COPY backend/ .

# Crea un directorio para los archivos estáticos del frontend
RUN mkdir -p frontend_static

# Copia los archivos del frontend al directorio estático del backend
COPY frontend/index.html frontend_static/
COPY frontend/script.js frontend_static/
# Si tienes más archivos CSS, imágenes, etc. en tu carpeta 'frontend', cópialos también:
# COPY frontend/styles.css frontend_static/styles.css
# COPY frontend/images/ frontend_static/images/

# Expone el puerto en el que FastAPI se ejecutará
EXPOSE 8000

# Comando para ejecutar la aplicación FastAPI
# Uvicorn servirá la aplicación y los archivos estáticos
CMD ["uvicorn", "backend_app:app", "--host", "0.0.0.0", "--port", "8000"]
