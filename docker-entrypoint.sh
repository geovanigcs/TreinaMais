#!/bin/bash

echo "Aguardando banco de dados..."
while ! pg_isready -h db -p 5432 -U treinamais_user; do
  sleep 1
done
echo "Banco de dados conectado!"

echo "Executando migrações..."
python manage.py migrate --noinput

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "Iniciando servidor Django..."
exec python manage.py runserver 0.0.0.0:8000
