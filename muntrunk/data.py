from typing import List
from pydantic import BaseModel
from .types import Semester
from .parse import parse_semester
from .scrape import fetch_banner

INITIAL_YEAR = 2000


class SemesterList(BaseModel):
    __root__: List[Semester]


def fetch_semester(year, term, level):
    result = fetch_banner(year, term, level)

    if not result:
        finished = True
    else:
        return parse_semester(result, year, term, level)


def fetch_all_semesters():
    semester_list = SemesterList(__root__=[])
    year = INITIAL_YEAR
    finished = False
    while not finished:
        for term in range(1, 3):
            for level in range(1, 3):
                semester_list.__root__.append(fetch_semester(year, term, level))
        year += 1
    return semester_list
