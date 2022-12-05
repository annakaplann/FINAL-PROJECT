import json
import os
import requests
import sqlite3
import matplotlib

API_KEY = "LZZ5WPD7HVNPP3QQ3KKE"

# https://api.songkick.com/api/3.0/search/venues.json?query={venue_name}&apikey=LZZ5WPD7HVNPP3QQ3KKE

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def get_capacity(venue_name):  
    url = f'https://api.songkick.com/api/3.0/search/venues.json?query={venue_name}&apikey={API_KEY}'

    resp = requests.get(url)
    data = json.loads(resp.text)
    print(data)
    # return data['capacity']

    # print('Exception')
    # return None
    
    tup = []
    for i in data['resultsPage']['results']:
        capacity = i['venue'][2]['capacity']
        tup.append((capacity))
    print(tup)
    return tup

def create_venue_table(cur,conn,cities):
    cur.execute("CREATE TABLE IF NOT EXISTS venue_data (id INTEGER PRIMARY KEY, name TEXT)")
    dict = []    
    names = get_capacity(cities)
    try:
        for name in names:
            dict.append(name)
    except:
        pass
    try:
        for i in range(1, len(dict)):
            cur.execute("INSERT OR IGNORE INTO venue_data (displayName,capacity) VALUES (?,?)",(i,dict[i-1]))
            conn.commit()
    except:
        pass

def main():
    cur, conn = setUpDatabase('database.db')
    event_id = 3003
    cities = get_capacity(event_id)
    create_venue_table(cur,conn,cities)
    print('Done')

    
if __name__ == "__main__":
    main()



