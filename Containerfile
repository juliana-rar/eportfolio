# Image for the "eportfolio" Django project
FROM python:3.12-slim

# No .pyc files and unbuffered output (real-time logs)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System dependencies:
#  - libpq5: PostgreSQL client runtime (psycopg2)
#  - libjpeg/zlib: image support for Pillow
#  - gettext: compilemessages for the ES/EN translations
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq5 \
        libjpeg62-turbo \
        zlib1g \
        gettext \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies first to take advantage of the layer cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code (in development the bind mount overrides it)
COPY . .

EXPOSE 8000

# The real command is defined in compose.yaml / compose.prod.yaml.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
