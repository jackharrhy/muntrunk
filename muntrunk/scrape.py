import shelve
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "github.com/jackharrhy/muntrunk",
    "Accept": "text/html",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://www5.mun.ca",
    "Connection": "keep-alive",
    "Referer": "https://www5.mun.ca/admit/hwswsltb.P_CourseSearch",
    "Upgrade-Insecure-Requests": "1",
}


def actually_fetch_banner(year, term, level):
    data = {
        "p_term": f"{year}0{term}",
        "p_levl": f"0{level}*00",
        "campus": "%",
        "faculty": "%",
        "prof": "%",
        "crn": "%",
    }

    response = requests.post(
        "https://www5.mun.ca/admit/hwswsltb.P_CourseResults", headers=headers, data=data
    )

    soup = BeautifulSoup(response.text, "html.parser")

    h2 = soup.find_all("h2")
    if len(h2) >= 2 and h2[1].text == "No matches were found for your search":
        return None

    return response


def fetch_banner(year, term, level):
    key = f"{year}_{term}_{level}"

    if year > 2030:  # spam prevent, sometime in the future fix this :)
        exit(1)

    with shelve.open("persist") as db:
        if not key in db:
            entire_resp = actually_fetch_banner(year, term, level)
            db[key] = entire_resp
            return entire_resp
        else:
            return db[key]
