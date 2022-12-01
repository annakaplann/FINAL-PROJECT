import json
import os
import requests
import sqlite3
import matplotlib

API_KEY = "LZZ5WPD7HVNPP3QQ3KKE"

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def get_city(event_id):    
    url = f'https://www.eventbriteapi.com/v3/events/{event_id}/?expand=venue'

    try: 
        resp = requests.get(url)
        data = json.loads(resp.text)
        return data['city']

    except: 
        print('Exception')
        return None

def get_event(event_id):
    url = f'https://www.eventbriteapi.com/v3/events/{event_id}/?expand=ticket_classes'

    try: 
        resp = requests.get(url)
        data = json.loads(resp.text)
        return data(['name'],['quantity_sold'])

    except: 
        print('Exception')
        return None

def create_city_table(cur,conn,cities):
    cur.execute("CREATE TABLE IF NOT EXISTS cities_data (id INTEGER PRIMARY KEY, name TEXT)")
    dict = []    
    names = get_city(cities)
    try:
        for name in names:
            dict.append(name)
    except:
        pass
    try:
        for i in range(1, len(dict)):
            cur.execute("INSERT OR IGNORE INTO cities_data (id,name) VALUES (?,?)",(i,dict[i-1]))
            conn.commit()
    except:
        pass

def main():
    cur, conn = setUpDatabase('database.db')
    event_id = 3003
    cities = get_city(event_id)
    create_city_table(cur,conn,cities)
    print('Done')

    
if __name__ == "__main__":
    main()



