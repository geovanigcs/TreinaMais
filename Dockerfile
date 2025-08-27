FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=treinamais.settings_docker

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        gcc \
        g++ \
        libc6-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements_simple.txt /app/
RUN pip install --no-cache-dir -r requirements_simple.txt
RUN pip install --no-cache-dir psycopg2-binary

COPY . /app/

RUN mkdir -p /app/staticfiles
RUN mkdir -p /app/media

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/docker-entrypoint.sh"]
