# backend/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ejecuta el script para crear el modelo
RUN python model.py

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

