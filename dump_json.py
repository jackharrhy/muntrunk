import logging
from muntrunk.types import Semester
from muntrunk.data import fetch_all_semesters
from typing import List
from pydantic import BaseModel

# logging.basicConfig(level=logging.DEBUG)

logging.disable(logging.DEBUG)

class SemesterList(BaseModel):
    __root__: List[Semester]

semester_list = SemesterList(__root__=[])

for semester in fetch_all_semesters():
    semester_list.__root__.append(semester)

print(semester_list.json())
