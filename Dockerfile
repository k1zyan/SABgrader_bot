FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install aiogram aiosqlite aiohttp
CMD ["python", "main.py"]
