# Usa Python 3.11 slim
FROM python:3.11-slim

# Carpeta de trabajo
WORKDIR /app

# Copiar requirements y instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar toda la aplicación dentro de un subdirectorio "app"
COPY . ./app

# Exponer el puerto de la API
EXPOSE 8000

# CMD para levantar FastAPI con OpenTelemetry
CMD ["opentelemetry-instrument", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]