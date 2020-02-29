import logging
import click
from muntrunk.types import Semester
from muntrunk.data import fetch_all_semesters, fetch_semester

# logging.basicConfig(level=logging.DEBUG)
logging.disable(logging.DEBUG)


@click.group()
def cli():
    pass


@cli.command()
@click.option("--year", default=2019)
@click.option("--term", default=2)
@click.option("--level", default=1)
def semester(year, term, level):
    print(fetch_semester(year, term, level).json())


@cli.command()
def everything():
    print(fetch_all_semesters().json())


if __name__ == "__main__":
    cli()
