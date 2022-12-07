import json
import os
import requests
import sqlite3
import matplotlib.pyplot as plt
import wiki

API_KEY = "ofpPfVqgtyHp/rCepavDTg==Rk0NxgPw543VyZez"

def setUpDatabase(database_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+database_name)
    cur = conn.cursor()
    return cur, conn

def get_population(city_list): 
    data = []
    lst = []
    for name in city_list:
        url = 'https://api.api-ninjas.com/v1/city?name={}'.format(name)
        resp = requests.get(url, headers={'X-Api-Key': 'ofpPfVqgtyHp/rCepavDTg==Rk0NxgPw543VyZez'})
        data = json.loads(resp.text)
        population = data[0]['population']
        name = data[0]['name']
        lst.append([name, population])
    return lst     

 
def create_population_table(lst, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS population_data (city TEXT PRIMARY KEY, population NUMBER)")
    limit = 0
    for city in lst:
        if limit < 25:
            city_name = city[0]
            population = city[1]
            rows = cur.execute("SELECT COUNT(*) FROM population_data")
            num = rows.fetchone()[0]
            cur.execute("INSERT OR IGNORE INTO population_data (city, population) VALUES (?, ?)", (str(city_name), str(population)))
            rows2 = cur.execute("SELECT COUNT(*) FROM population_data")
            num2 = rows2.fetchone()[0]
            if num2 > num:
                limit += 1
            conn.commit()
'''
def visualization(cur, conn):
    # cur.execute("SELECT city, population FROM population_data")
    calc_dict = wiki.percent_calculations("calculations.txt", cur, conn)

    # data = cur.fetchall()
    data2 = sorted(calc_dict.items(), key = lambda x: x[1], reverse=True)
    # conn.commit()
    
    city_list = []
    population_list = []
    for city, percent in data2:
        if len(city_list) < 10:
            city_list.append(city)
            population_list.append(percent)
    
    plt.figure()
    plt.bar(city_list, population_list, color = 'lightblue')
    plt.title("Percent Calculation of Concert Attendance by City Population")
    plt.xlabel("Cities")
    plt.ylabel("Population")
    plt.xticks(rotation = 45)
    plt.tight_layout()
    plt.colorbar
    # plt.show()
    plt.savefig('PercentCalculations')
'''

def main():
    cur, conn = setUpDatabase('concerts.db')
    city_list = ['San Francisco', 'Los Angeles', 'Nashville', 'Chicago', 'New York', 
    'Boston', 'Amsterdam', 'Tokyo', 'Paris', 'Stockholm', 
    'Copenhagen', 'Melbourne', 'Hamburg', 'Barcelona', 'Dublin', 
    'Milan', 'Munich', 'Singapore', 'Madrid', 'Dallas',
    'Santiago', 'Detroit', 'Denver', 'Seattle', 'Vancouver', 
    'Sacramento', 'Philadelphia', 'Cleveland', 'Atlanta', 'Pittsburgh', 
    'Milwaukee', 'Portland', 'Houston', 'Manchester', 'Budapest', 
    'Prague', 'London', 'Toronto', 'Lisbon', 'Inglewood', 
    'New York', 'Mexico City', 'St. Louis', 'Tampa', 'Hershey', 
    'Duluth', 'Indianapolis', 'Sao Paulo', 'Cali', 'Birmingham',
    'Mannheim', 'Hong Kong', 'Perth', 'Brisbane', 'Kobe', 
    'Chiba', "Manila", 'Bologna', 'Oberhausen', 'Auckland', 
    'Antwerp', 'Tianjin', 'Lahore', 'Shenzhen', 'San Juan', 
    'Naples', 'Lagos', 'Kinshasa', 'Karachi', 'Osaka', 
    'Cairo', 'Mumbai', 'Nagoya', 'Seoul', 'Chennai',
    'Brasilia', 'Cape Town', 'Tel Aviv', 'Montreal', 'Porto Alegre', 
    'Salvador', 'Dubai', 'Depok', 'Bursa', 'Minsk',
    'Vienna', 'Tanger', 'Rabat', 'Jilin', 'Rosario',
    'Harare', 'Natal', 'Ottawa', 'Zurich', 'Sofia', 
    'Omsk', 'Ufa', 'Cologne', 'Chihuahua', 'Leshan', 'Las Vegas']
    data = get_population(city_list)
    create_population_table(data,cur,conn)
    #visualization(cur, conn)
    #calculations("calculations.txt", cur, conn)
    # file = open("calculations.txt", "r")
    # print(file.read())
    # file.close()
    print('Done')
    
main()




