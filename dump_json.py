import logging
import click
from muntrunk.types import Semester
from muntrunk.data import fetch_all_semesters, fetch_semester
from typing import List
from pydantic import BaseModel

# logging.basicConfig(level=logging.DEBUG)
logging.disable(logging.DEBUG)


class SemesterList(BaseModel):
    __root__: List[Semester]


semester_list = SemesterList(__root__=[])


@click.group()
def cli():
    pass


@cli.command()
@click.option("--year", default=2019)
@click.option("--term", default=2)
@click.option("--level", default=1)
def semester(year, term, level):
    semester_list.__root__.append(list(fetch_semester(year, term, level)))
    print(semester_list.json())


@cli.command()
def everything():
    for semester in fetch_all_semesters():
        semester_list.__root__.append(semester)
    print(semester_list.json())


if __name__ == "__main__":
    cli()
