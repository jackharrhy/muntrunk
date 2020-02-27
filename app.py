import logging
from muntrunk.types import Semester
from muntrunk.data import fetch_all_semesters
from typing import List
from pydantic import BaseModel
from flask import Flask, jsonify

logging.disable(logging.DEBUG)

class SemesterList(BaseModel):
    __root__: List[Semester]

semester_list = SemesterList(__root__=[])

for semester in fetch_all_semesters():
    semester_list.__root__.append(semester)

app = Flask(__name__)


@app.route("/")
def get_entire_list():
    return semester_list.json()
