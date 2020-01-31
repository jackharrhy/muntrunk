# muntrunk

**because self-service is a _pain_**

![](https://github.com/jackharrhy/muntrunk/workflows/Deploy%20to%20Dockerhub/badge.svg)

----

_this is currently a work in progress!_

currently, its only built to parse the current semester, obv. that's no good :)

- `app.py` - flask app to serve w2020 semester as json to the _world_
- `dump_json.py` - dump entire w2020 semester as json to file
- `populate_db.py` - dump entire w2020 semester to a postgresql database
- `muntrunk/` - the _brains_
