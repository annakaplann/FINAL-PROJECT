import json
import os
import requests
import sqlite3
import matplotlib
import re
import sys

api_key = "Mjk2NjIyNTN8MTY2OTY3Nzg5Mi40OTk3MTM0"

def get_state():
    url = f'https://api.seatgeek.com/2/events?per_page=1000&client_id={api_key}'
    try:
        resp = requests.get(url)
        data = json.loads(resp.text)
    except:
        return None
    city_lst = []
    for item in data['events']:
        city_lst.append(item['venue']['state'])
    #print(city_lst)
    return city_lst

def get_score(first_name, last_name):
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
    return tup

def make_database(database_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+database_name)
    cur = conn.cursor()
    return cur, conn

def make_state_id_table(data, cur, conn):
    state_list = []
    limit = 0
    for state in data:
        if state not in state_list:
            state_list.append(state)
    cur.execute("CREATE TABLE IF NOT EXISTS State_id (state_id INTEGER PRIMARY KEY, state TEXT)")
    for x in range(len(state_list)):
        if limit < 25:
            cur.execute("INSERT OR IGNORE INTO State_id (state_id, state) VALUES (?, ?)", (x,state_list[x]))
            limit += 1
    conn.commit()

def make_location_table(data, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Location_scores (date TEXT PRIMARY KEY, location_id TEXT, score NUMBER)")
    limit = 0
    for concert in data:
        if limit < 25:
            date = concert[2]
            cur.execute("SELECT state_id FROM State_id WHERE state = ?", (concert[0],))
            location_id = int(cur.fetchone()[0])
            score = concert[1]
            cur.execute("INSERT OR IGNORE INTO Location_scores (date, location_id, score) values(?, ?, ?)", (date, location_id, score))
            limit += 1
    conn.commit()


def main():
    state_data = get_state()
    taylor_data = get_score("taylor", "swift")
    cur, conn = make_database("concerts.db")
    make_state_id_table(state_data, cur, conn)
    count = cur.execute("SELECT COUNT(*) FROM State_id")
    if count != 55:
        make_state_id_table(state_data, cur, conn)
        sys.exit()
    make_location_table(taylor_data, cur, conn)
    



if __name__ == "__main__":
    main()





