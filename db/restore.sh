#!/usr/bin/env sh
. ./.env
psql "$POSTGRES_HOST_DATABASE_URL" < dump.pgsql
