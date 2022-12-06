import json
import os
import requests
import sqlite3
import matplotlib
import re
import sys

api_key = "Mjk2NjIyNTN8MTY2OTY3Nzg5Mi40OTk3MTM0"

def get_venue():
    url = f'https://api.seatgeek.com/2/venues?per_page=101&client_id={api_key}'
    try:
        resp = requests.get(url)
        data = json.loads(resp.text)
    except:
        return None
    venue_lst = []
    for item in data['venues']:
        venue = item['name']
        city = item['city']
        score = item['score']
        venue_lst.append((venue, city, score))
    #print(venue_lst)
    return venue_lst

'''def get_score(first_name, last_name):
    url = f'https://api.seatgeek.com/2/events?per_page=100&performers.slug={first_name}-{last_name}&client_id={api_key}'
    try:
        resp = requests.get(url)
        data = json.loads(resp.text)
        #print(data)
    except:
        return None
    tup = []
    for item in data['events']:
        old_date = item['datetime_utc']
        reg_ex = "(\d{4}-\d{2}-\d{2}).*"
        date = re.findall(reg_ex, old_date)
        city = item['venue']['state']
        score = item['venue']['score']
        tup.append((city,score,date[0]))
    #print(tup)
    return tup'''

def make_database(database_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+database_name)
    cur = conn.cursor()
    return cur, conn

def make_venue_id_table(data, cur, conn):
    venue_list = []
    limit = 0
    for venue in data:
        if venue[0] not in venue_list:
            venue_list.append(venue[0])
    cur.execute("CREATE TABLE IF NOT EXISTS Venue_id (venue_id INTEGER PRIMARY KEY, venue TEXT)")
    for x in range(len(venue_list)):
        if limit < 25:
            cur.execute("INSERT OR IGNORE INTO Venue_id (venue_id, venue) VALUES (?, ?)", (x,venue_list[x]))
            limit += 1
            conn.commit()

def make_location_table(data, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Location_scores (location_id INTEGER PRIMARY KEY, city TEXT, score NUMBER)")
    limit = 0
    for concert in data:
       if limit < 25:
            cur.execute("SELECT venue_id FROM Venue_id WHERE venue = ?", (concert[0],))
            location_id = int(cur.fetchone()[0])
            city = concert[1]
            score = concert[2]
            cur.execute("INSERT OR IGNORE INTO Location_scores (location_id, city, score) values(?, ?, ?)", (location_id, city, score))
            limit += 1
            conn.commit()


def main():
    venue_data = get_venue()
    cur, conn = make_database("concerts.db")
    make_venue_id_table(venue_data, cur, conn)
    make_location_table(venue_data, cur, conn)
    
    



if __name__ == "__main__":
    main()





