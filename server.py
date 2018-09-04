from flask import Flask, Response

import json
from collections import OrderedDict
from datetime import timezone, timedelta, datetime
from dateutil import parser

app = Flask(__name__)

gmt = timezone(timedelta(0), "GMT")

def date_response(dt):
  return Response(json.dumps(
    OrderedDict([
      ("unix", int(dt.timestamp() * 1000)),
      ("utc", dt.astimezone(gmt).strftime("%a, %d %b %Y %H:%M:%S %Z"))
    ])),
  mimetype='application/json'
  )

@app.route("/api/timestamp/", defaults={'date_string': None})
@app.route("/api/timestamp/<date_string>/")
def date(date_string):
  if date_string:
    try:
      stamp = int(float((date_string)))
      d = datetime(1970, 1, 1, 0, 0, 0, tzinfo=gmt) +\
          timedelta(milliseconds=stamp)
      d = d.replace(tzinfo=gmt)
      return date_response(d)
    except ValueError as e:
      print(e)
      try:
        d = parser.parse(date_string)
        d = d.replace(tzinfo=gmt)
        return date_response(d)
      except ValueError as e:
        print(e)
        return Response(
            json.dumps({"error": "Invalid Date"}),
            mimetype='application/json'
        ), 400
  else:
    # If no date string was specified, return the response for now()
    d = datetime.now(gmt)
    return date_response(d)
    

if __name__ == "__main__":
  app.run()
