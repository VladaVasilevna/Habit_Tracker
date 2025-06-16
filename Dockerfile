# Используем официальный Python образ
FROM python:3.11-slim

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

# Собираем статику (если есть)
RUN python manage.py collectstatic --noinput

# Открываем порт
EXPOSE 8000

# Команда запуска Django
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]

# Устанавливает переменную окружения, которая гарантирует, что вывод из python будет отправлен прямо в терминал без предварительной буферизации
ENV PYTHONUNBUFFERED 1
