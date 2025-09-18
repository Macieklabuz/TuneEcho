FROM python:3.11-slim

WORKDIR /app

# Dependencje Pythona
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Kod aplikacji
COPY backend /app/backend

# Katalog na dane (mapowany przez docker-compose)
RUN mkdir -p /app/data

EXPOSE 8000
ENV PYTHONUNBUFFERED=1

# Uruchomienie przez gunicorn
CMD ["gunicorn", "backend.app:app", "-b", "0.0.0.0:8000", "-w", "2"]
