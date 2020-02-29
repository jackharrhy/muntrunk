import logging
import click
from muntrunk.types import Semester, common_types
from muntrunk.data import fetch_all_semesters, fetch_semester

logging.basicConfig(level=logging.DEBUG)


@click.group()
def cli():
    pass


@cli.command()
@click.option("--year", default=2019)
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
