# syntax=docker/dockerfile:1

FROM python:3.10-alpine

WORKDIR /server

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY src src
COPY utils utils
COPY setup_db.py setup_db.py

RUN python3 setup_db.py

ENV IP="0.0.0.0"
ENV NUMBER_OF_WORKERS=2

EXPOSE 8080

ENTRYPOINT gunicorn -w ${NUMBER_OF_WORKERS} -b ${IP}:8080 src.app:app