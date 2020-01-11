import shelve
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://www5.mun.ca",
    "Connection": "keep-alive",
    "Referer": "https://www5.mun.ca/admit/hwswsltb.P_CourseSearch?p_term=201902&p_levl=01*04",
    "Upgrade-Insecure-Requests": "1",
}

data = {
    "p_term": "201902",
    "p_levl": "01*04",
    "campus": "St. John's",
    "faculty": "%",
    "prof": "%",
    "crn": "%",
}


def fresh_entire_resp():
    return requests.post(
        "https://www5.mun.ca/admit/hwswsltb.P_CourseResults", headers=headers, data=data
    )


def grab_entire_resp():
    with shelve.open("persist") as db:
        if not "entire_resp" in db:
            entire_resp = fresh_entire_resp()
            db["entire_resp"] = entire_resp
            return entire_resp
        else:
            return db["entire_resp"]