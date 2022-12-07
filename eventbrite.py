import json
import os
import requests
import sqlite3
import matplotlib

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
def calculations(filename, cur, conn):
    cur.execute("SELECT population_data.city, population_data.population, Harry_Styles.attendance FROM population_data JOIN Harry_Styles ON Harry_Styles.city == population_data.city")
    results = cur.fetchall()
    for result in results:
        city = result[0]
        percentage = round((result[2] / result[1]), 4)
        f = open(filename, "w")
        f.write("Percentage of City Population Who Attended Concert\n")
        f.write(city+": "+str(percentage)+"\n")
    f.close()
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
    #calculations("calculations.txt", cur, conn)
    # file = open("calculations.txt", "r")
    # print(file.read())
    # file.close()
    print('Done')
    
main()




