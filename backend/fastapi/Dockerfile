
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-alpine3.14-2024-03-11

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]