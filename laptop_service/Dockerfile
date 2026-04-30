FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Generate migrations, apply them, seed the database, and start the server
CMD ["sh", "-c", "python manage.py makemigrations --noinput && python manage.py migrate --noinput && python seed_db.py && python seed_graph.py && python manage.py runserver 0.0.0.0:8000"]
