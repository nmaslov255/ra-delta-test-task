FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/django

COPY requirements.txt /usr/src/django/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/django/

WORKDIR /usr/src/django/apps

RUN python manage.py migrate

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "apps.wsgi"]
