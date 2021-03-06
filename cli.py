import logging
import click

from dotenv import load_dotenv

load_dotenv()

from muntrunk.types import Semester, common_types
from muntrunk.data import fetch_all_semesters, fetch_semester
from muntrunk.db import db_drop_all
from muntrunk.populate import db_populate_all_semesters

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@click.group()
def cli():
    pass


@cli.command()
def db_populate():
    db_populate_all_semesters()


@cli.command()
def db_drop():
    db_drop_all()


@cli.command()
@click.option("--year", default=2020)
@click.option("--term", default=2)
@click.option("--level", default=1)
@click.option("--onlytypes", default=False)
def jsondump_semester(year, term, level, onlytypes):
    logging.disable(logging.DEBUG)
    all_semesters = fetch_semester(year, term, level)
    if not onlytypes:
        print(all_semesters.json())
    else:
        print(common_types.json())


@cli.command()
def jsondump_all():
    logging.disable(logging.DEBUG)
    print(fetch_all_semesters().json())


if __name__ == "__main__":
    cli()
