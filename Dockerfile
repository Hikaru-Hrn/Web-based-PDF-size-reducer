# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем Ghostscript
RUN apt-get update && apt-get install -y \
    ghostscript \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY packages/core /app/packages/core
RUN pip install -e /app/packages/core
COPY . .

# Копируем проект
COPY . .

# Создаем папку для загрузок
RUN mkdir -p uploads

# Запускаем приложение
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
