FROM node:14-alpine3.11 as website-build

WORKDIR /build

COPY ./course-cook/package*.json /build/
RUN npm install --silent
COPY ./course-cook/*.js /build/
COPY ./course-cook/*.html /build/
COPY ./course-cook/src/ /build/src/
RUN npm run build

FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine-2020-08-16

WORKDIR /app

RUN mkdir -p course-cook/dist/
COPY --from=website-build /build/dist /app/course-cook/dist/

COPY ./muntrunk /app/muntrunk/
COPY ./app.py /app/main.py
COPY ./requirements.txt /app
COPY ./hasura-metadata.json /app/hasura-metadata.json
COPY ./uwsgi.ini /app/uwsgi.ini

RUN apk update && \
  apk add postgresql-libs && \
  apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
  python3 -m pip install -r requirements.txt --no-cache-dir && \
  apk --purge del .build-deps
