FROM python:3.12-slim-bookworm

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y postgresql-client


CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:8000", "web.wsgi:application"]
