FROM python:3.12 as base

ENV DIR=/app
WORKDIR $DIR


# DEVELOPMENT
FROM base as dev

ENV PYTHON_ENV=development

RUN apt-get update && apt-get install
COPY requirements-dev.txt .

RUN pip install -r requirements-dev.txt
COPY . .

CMD ["python", "./app/main.py"]


# PRODUCTION
FROM base as production

ENV PYTHON_ENV=production

RUN apt-get update && apt-get install
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["python ", "./app/main.py"]
