# Використовуємо офіційний Python образ з базовою версією
FROM python:3.11

# Встановлюємо залежності Poetry
RUN pip install poetry

# Створюємо директорію для нашого проекту
WORKDIR /app

# Копіюємо файли проекту до контейнера
COPY . /app

# Встановлюємо залежності за допомогою Poetry
RUN poetry install --no-root

# Запускаємо "Персональний помічник"
CMD ["poetry", "run", "python", "my_bot/main.py"]
