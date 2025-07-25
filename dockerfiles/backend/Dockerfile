FROM python:3.13-alpine3.22

WORKDIR /backend

COPY ../../requirements/requirements.txt /backend/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ../../backend /backend
