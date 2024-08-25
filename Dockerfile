FROM python:3.10.14-alpine3.20

WORKDIR /app

COPY . .

EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r requirements.txt --no-cache-dir

RUN adduser --disabled-password kode-user

USER kode-user
