import json
import os
import requests
import sqlite3
import matplotlib

api_key = "Mjk2NjIyNTN8MTY2OTY3Nzg5Mi40OTk3MTM0"

def get_venue_and_city(first_name, last_name):
    url = f'https://api.seatgeek.com/2/events?performers.slug={first_name}-{last_name}&client_id={api_key}'
    try:
        resp = requests.get(url)
        data = json.loads(resp.text)
        #print(data)
    except:
        return None
    tup = []
    for item in data['events']:
        city = item['venue']['city']
        score = item['venue']['score']
        tup.append((city,score))
    print(tup)
    return tup


get_venue_and_city("justin", "bieber")


"https://api.seatgeek.com/2/events?performers.slug=justin-bieber&client_id=Mjk2NjIyNTN8MTY2OTY3Nzg5Mi40OTk3MTM0"





