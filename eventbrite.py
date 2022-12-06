import json
import os
import requests
import sqlite3
import matplotlib

API_KEY = "ofpPfVqgtyHp/rCepavDTg==Rk0NxgPw543VyZez"

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def get_population(name): 
    url = 'https://api.api-ninjas.com/v1/city?name={}'.format(name)
    resp = requests.get(url, headers={'X-Api-Key': 'ofpPfVqgtyHp/rCepavDTg==Rk0NxgPw543VyZez'})
    print(resp)
    data = json.loads(resp.text)
    tup = []
    if resp.status_code == requests.codes.ok:
        print(resp.text)
        for i in data:
            population = i['population']
            tup.append((population))
        return tup
    else:
        print("Error:", resp.status_code, resp.text)     
    
def create_population_table(cur,conn,cities):
    cur.execute("CREATE TABLE IF NOT EXISTS population_data (id INTEGER PRIMARY KEY, name TEXT)")
    dict = []    
    names = get_population(cities)
    try:
        for name in names:
            dict.append(name)
    except:
        pass
    try:
        for i in range(1, len(dict)):
            cur.execute("INSERT OR IGNORE INTO population_data (displayName,capacity) VALUES (?,?)",(i,dict[i-1]))
            conn.commit()
    except:
        pass

def main():
    cur, conn = setUpDatabase('database.db')
    name = "San Francisco"
    cities = get_population(name)
    create_population_table(cur,conn,cities)
    print('Done')

    
if __name__ == "__main__":
    main()



