import shelve
import logging
from typing import List

from pydantic import BaseModel

from .types import Semester
from .parse import parse_semester
from .scrape import fetch_banner

logger = logging.getLogger(__name__)

INITIAL_YEAR = 2000


class SemesterList(BaseModel):
    __root__: List[Semester]


def fetch_semester(year, term, level):
    result = fetch_banner(year, term, level)

    with shelve.open("fetch_semester") as db:
        if not result:
            return None

        if not key in db:
            logger.debug(f"fetch_semester - actually parsing data...")
            semester = parse_semester(result, year, term, level)
            db[key] = semester
            return semester
        else:
            logger.debug(f"fetch_semester - semester already parsed")
            return db[key]


def fetch_all_semesters():
    semester_list = SemesterList(__root__=[])
    year = INITIAL_YEAR
    finished = False
    while not finished:
        for term in range(1, 3):
            for level in range(1, 3):
                should_be_semester = fetch_semester(year, term, level)

                if not should_be_semester:
                    finished = True
                else:
                    semester_list.__root__.append(should_be_semester)

        year += 1

    return semester_list
