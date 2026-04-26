FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir flask psycopg2-binary python-dotenv

EXPOSE 5000

CMD ["python", "app.py"]