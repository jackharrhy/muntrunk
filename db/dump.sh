#!/usr/bin/env sh
. ./.env
pg_dump "$POSTGRES_HOST_DATABASE_URL" > dump.pgsql
