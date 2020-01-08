FROM tiangolo/uwsgi-nginx-flask:python3.7-alpine3.7

WORKDIR /app
COPY app.py /app/main.py
COPY requirements.txt /app

RUN pip install -r requirements.txt
