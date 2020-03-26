FROM tiangolo/uwsgi-nginx-flask:python3.7-alpine3.7

WORKDIR /app
COPY muntrunk /app/muntrunk
COPY app.py /app/main.py
COPY requirements.txt /app
RUN apk add gcc libpq linux-headers musl-dev postgresql-dev python3-dev
RUN pip install -r requirements.txt
