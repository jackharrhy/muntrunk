from dotenv import load_dotenv

load_dotenv()

import logging
import os
import time
import atexit

from flask import Flask, jsonify, request
import requests

from muntrunk.db import init_tables, db_drop_all
from muntrunk.populate import db_populate_all_semesters

from apscheduler.schedulers.background import BackgroundScheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='./course-cook/dist/', static_url_path='/')

HASURA_GRAPHQL_URI = os.getenv("HASURA_GRAPHQL_URI")
HASURA_ADMIN_SECRET = os.getenv("HASURA_GRAPHQL_ADMIN_SECRET")
HASURA_ADMIN_SECRET_HEADER = "X-Hasura-Admin-Secret"
HASURA_HEADERS = headers = {
    HASURA_ADMIN_SECRET_HEADER: HASURA_ADMIN_SECRET,
}

with open("./hasura-metadata.json", "r") as file:
    HASURA_METADATA = file.read()

is_refreshing = False


def refresh_hasura():
    logger.info("replacing hasura metadata...")
    data = '{"type": "replace_metadata", "args": ' + HASURA_METADATA + "}"
    r = requests.post(f"{HASURA_GRAPHQL_URI}/v1/query", headers=headers, data=data)


def refresh():
    global is_refreshing
    is_refreshing = True

    logger.info("refresing...")
    try:
        logger.info("dropping public schema...")
        db_drop_all()
        logger.info("recreating tables...")
        init_tables()

        logger.info("populating back semesters")
        db_populate_all_semesters()

        refresh_hasura()

        logger.info("finished refresing!")
    finally:
        is_refreshing = False


@app.route("/hasura-auth")
def hasura_auth():
    return jsonify({"X-Hasura-Role": "anonymous"})


@app.route("/is-refreshing")
def check_if_refreshing():
    global is_refreshing

    return str(is_refreshing)


@app.route("/manual-refresh")
def manual_refresh():
    secret = request.headers.get(HASURA_ADMIN_SECRET_HEADER)

    if secret != HASURA_ADMIN_SECRET:
        return f"Invalid {HASURA_ADMIN_SECRET_HEADER} Header", 403

    global is_refreshing

    if is_refreshing:
        return "already refreshing", 400
    else:
        refresh()

    return "", 204

@app.route('/')
def index():
    return app.send_static_file('index.html')

scheduler = BackgroundScheduler()
scheduler.add_job(func=refresh, trigger="interval", hours=24)
scheduler.start()

refresh_hasura()

atexit.register(lambda: scheduler.shutdown())
