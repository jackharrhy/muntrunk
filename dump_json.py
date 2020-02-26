import logging

logging.basicConfig(level=logging.DEBUG)

from muntrunk.data import fetch_all_semesters

for semester in fetch_all_semesters():
    print(semester.json())
