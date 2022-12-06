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


def get_population(city_list): 
      #make one list
    data = []
    # population_list = []
    # name_list = [] 
    for name in city_list:
        url = 'https://api.api-ninjas.com/v1/city?name={}'.format(name)
        resp = requests.get(url, headers={'X-Api-Key': 'ofpPfVqgtyHp/rCepavDTg==Rk0NxgPw543VyZez'})
        #print(resp)
        data = json.loads(resp.text)
        print(data)
        #if resp.status_code == requests.codes.ok:
            #print(resp.text)
            #print(data[0])
        population = data[0]['population']
        name = data[0]['name']
        data.append([(name, population)])
        #else:
            #print("Error:", resp.status_code, resp.text) 
    print(data)
    return data       
    
def create_population_table(data, cur,conn):
    cur.execute("CREATE TABLE IF NOT EXISTS population_data (city TEXT PRIMARY KEY, population TEXT)")
    #limit = 0
    for pop in data:
        print(pop)
        #if limit < 25:
        city = pop[0]
        population = pop[1]
        #rows = cur.execute("SELECT COUNT(*) FROM population_data")
        #num = rows.fetchone()[0]
        cur.execute("INSERT OR IGNORE INTO population_data (city, population) VALUES (?, ?)", (city, population))
        conn.commit()

# def calculations(filename, cur, conn):
#     pop_dict = {}
#     cur.execute("SELECT city, population FROM population_data")
#     results = cur.fetchall()
#     for result in results:
#         if result[0] not in pop_dict:
#             pop_dict[result[0]] = 0
#         pop_dict[result[0]] += result[1]
#     f = open(filename, "w")
#     f.write("Population of Cities Based On Concert Venues\n")
#     for pop in pop_dict:
#         f.write(pop+": "+str(pop_dict[pop])+"\n")
#     f.close()


def main():
    cur, conn = setUpDatabase('concerts.db')
    city_list = ['San Francisco', 'Los Angeles', 'Nashville', 'Chicago', 'New York', 'Boston']
    data = get_population(city_list)
    create_population_table(data,cur,conn)
    # calculations("calculations.txt", cur, conn)
    # file = open("calculations.txt", "r")
    # print(file.read())
    # file.close()
    print('Done')
    
main()




