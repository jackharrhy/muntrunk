#!/usr/bin/env sh
. ./.env
pg_dump "$HOST_DATABASE_URL" > dump.pgsql
