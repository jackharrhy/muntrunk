#!/usr/bin/env sh
. ./.env
psql "$POSTGRES_HOST_DATABASE_URL" -c "CREATE USER $PGQL_USER WITH PASSWORD '$PGQL_PASSWORD'"
psql "$POSTGRES_HOST_DATABASE_URL" -c "GRANT CONNECT ON DATABASE $PGQL_DB TO $PGQL_USER"
psql "$POSTGRES_HOST_DATABASE_URL" -c "GRANT USAGE ON SCHEMA public TO $PGQL_USER"
psql "$POSTGRES_HOST_DATABASE_URL" -c "GRANT SELECT ON ALL TABLES IN SCHEMA public TO $PGQL_USER"
