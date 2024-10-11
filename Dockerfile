# Usa una imagen base de Python
FROM python:3.9-slim

# Instala las dependencias de sistema
RUN apt-get update && apt-get install -y \
    libpq-dev gcc

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo requirements.txt
COPY requirements.txt /app/

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del proyecto
COPY . /app

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
