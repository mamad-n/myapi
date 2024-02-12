FROM python:3.8-alpine

RUN  mkdir /app

WORKDIR /app

COPY ./requirements.txt .

# RUN apk update && apk add gcc  libpq-dev 

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

ENTRYPOINT /bin/sh ./entrypoint.sh

