import json
import os
import requests
import sqlite3
import matplotlib.pyplot as plt

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

def make_city_id_table(data, cur, conn):
    city_list = []
    limit = 0
    for city in data:
        if city[0] not in city_list:
            city_list.append(city[0])
    cur.execute("CREATE TABLE IF NOT EXISTS City_id (city_id INTEGER PRIMARY KEY, city TEXT UNIQUE)")
    for x in range(len(city_list)):
        if limit < 25:
            rows = cur.execute("SELECT COUNT(*) FROM City_id")
            num = rows.fetchone()[0]
            cur.execute("INSERT OR IGNORE INTO City_id (city_id, city) VALUES (?, ?)", (None,city_list[x]))
            rows2 = cur.execute("SELECT COUNT(*) FROM City_id")
            num2 = rows2.fetchone()[0]
            if num2 > num:
                limit += 1
            conn.commit()

def create_population_table(lst, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS population_data (city_id INTEGER PRIMARY KEY, population NUMBER)")
    limit = 0
    for city in lst:
        if limit < 25:
            cur.execute("SELECT city_id FROM City_id WHERE city = ?", (city[0],))
            city_id = int(cur.fetchone()[0])
            population = city[1]
            rows = cur.execute("SELECT COUNT(*) FROM population_data")
            num = rows.fetchone()[0]
            cur.execute("INSERT OR IGNORE INTO population_data (city_id, population) VALUES (?, ?)", (city_id, str(population)))
            rows2 = cur.execute("SELECT COUNT(*) FROM population_data")
            num2 = rows2.fetchone()[0]
            if num2 > num:
                limit += 1
            conn.commit()

def visualization(cur, conn):
    cur.execute("SELECT population_data.city_id, population_data.population, Harry_Styles.attendance FROM population_data JOIN Harry_Styles ON Harry_Styles.city_id == population_data.city_id")
    results = cur.fetchall()
    percentages = {}
    for result in results:
        cur.execute("SELECT city FROM City_id WHERE city_id = ?", (result[0],))
        city= cur.fetchone()[0]
        percentage = round((result[2] / result[1]), 4)
        percentages[city] = percentage
    sorted_percentages = sorted(percentages.items(), key = lambda x: x[1], reverse=True)
    city_list = []
    percentages_list = []
    for item in sorted_percentages:
        if len(city_list) < 12:
            city_list.append(item[0])
            percentages_list.append(item[1])
    
    plt.figure()
    plt.bar(city_list, percentages_list, color = 'lightblue')
    plt.title("Proportion of City Population That Attended Concert")
    plt.xlabel("Cities")
    plt.ylabel("Population Proportion")
    plt.xticks(rotation = 45)
    plt.tight_layout()
    plt.colorbar
    plt.savefig('PercentCalculations')


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
    make_city_id_table(data, cur, conn)
    create_population_table(data,cur,conn)
    visualization(cur, conn)
    print('Done')
    
main()




