from .parse import parse_semester
from .scrape import fetch_banner

INITIAL_YEAR = 2000


def fetch_all_semesters():
    year = INITIAL_YEAR
    finished = False
    while not finished:
        for term in range(1, 3):
            for level in range(1, 3):
                result = fetch_banner(year, term, level)

                if not result:
                    finished = True
                else:
                    yield parse_semester(result)

        year += 1
