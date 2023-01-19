FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY requirements.txt requirements.txt

RUN apt-get update && \
    apt-get -y install gcc

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8000

COPY . /code/

