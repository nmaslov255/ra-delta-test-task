FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update
RUN apt install -y default-mysql-client
RUN apt install -y netcat

WORKDIR /usr/src/django
COPY . /usr/src/django/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/django/apps