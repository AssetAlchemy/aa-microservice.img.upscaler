FROM python:3.13.0-alpine3.20 as base

ENV DIR=/app
WORKDIR $DIR


# DEVELOPMENT
FROM base as dev

ENV PYTHON_ENV=development

RUN apk update && apk upgrade
COPY requirements-dev.txt .

RUN pip install -r requirements-dev.txt
COPY . .

CMD ["python", "./app/main.py"]


# PRODUCTION
FROM base as production

ENV PYTHON_ENV=production

RUN apk update && apk upgrade
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["python ", "./app/main.py"]
