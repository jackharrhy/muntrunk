#!/usr/bin/env sh
. ./.env
psql "$HOST_DATABASE_URL" < dump.pgsql
