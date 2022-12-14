from bs4 import BeautifulSoup
import os
import re
import requests
import sqlite3
import matplotlib.pyplot as plt

def concert_data():

    resp = requests.get('https://en.wikipedia.org/wiki/Love_On_Tour')
    soup = BeautifulSoup(resp.text, 'html.parser')
    table_tags = soup.find_all('table', class_ = 'wikitable plainrowheaders')
    resp2 = requests.get('https://en.wikipedia.org/wiki/Harry_Styles:_Live_on_Tour')
    soup = BeautifulSoup(resp2.text, 'html.parser')
    table_tags2 = soup.find_all('table', class_ = 'wikitable')
    data = []

    #HARRY STYLES LIVE ON TOUR 2017 & 2018
    for table in table_tags2:
        for concert in table.find_all('tr'):
            concert_info = concert.find_all('td')
            if len(concert_info) >= 5 and len(concert_info) <= 7:
                date = concert_info[0].text.strip()
                city = concert_info[1].text.strip()
                pattern = "(\d*,\d*) / .*"
                tickets = concert_info[-2].text.strip()
                tickets_sold = re.findall(pattern, tickets)
                pattern2 = ".* / (\d*,\d*)"
                capacity = re.findall(pattern2, tickets)
                if tickets_sold != []:
                    number = re.sub(",", "", tickets_sold[0])
                    number2 = re.sub(",", "", capacity[0])
                    data.append([date, city, int(number), int(number2)])

    #HARRY STYLES LOVE ON TOUR 2021 & 2022
    for table in table_tags:
        for concert in table.find_all('tr'):
            concert_date = concert.find_all('th')
            concert_info = concert.find_all('td')
            if concert_info != []:
                date = concert_date[0].text.strip()
                city = concert_info[0].text.strip()
                pattern = "(\d*,\d*) / .*"
                tickets = concert_info[-2].text.strip()
                tickets_sold = re.findall(pattern, tickets)
                pattern2 = ".* / (\d*,\d*)"
                capacity = re.findall(pattern2, tickets)
                if tickets_sold != []:
                    number = re.sub(",", "", tickets_sold[0])
                    number2 = re.sub(",", "", capacity[0])
                    data.append([date, city, int(number), int(number2)])
    return data

def make_database(database_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+database_name)
    cur = conn.cursor()
    return cur, conn

def make_city_id_table(data, cur, conn):
    city_list = []
    for city in data:
        if city[1] not in city_list:
            city_list.append(city[1])
    cur.execute("CREATE TABLE IF NOT EXISTS City_id (city_id INTEGER PRIMARY KEY, city TEXT UNIQUE)")
    limit = 0
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

def make_table(data, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Harry_Styles (date TEXT PRIMARY KEY, city_id INTEGER, attendance INTEGER, capacity INTEGER)")
    limit = 0
    for concert in data:
        if limit < 25:
            date = concert[0]
            cur.execute("SELECT city_id FROM City_id WHERE city = ?", (concert[1],))
            city_id = int(cur.fetchone()[0])
            attendance = concert[2]
            capacity = concert[3]
            rows = cur.execute("SELECT COUNT(*) FROM Harry_Styles")
            num = rows.fetchone()[0]
            cur.execute("INSERT OR IGNORE INTO Harry_Styles (date, city_id, attendance, capacity) VALUES (?, ?, ?, ?)", (date, city_id, attendance, capacity))
            rows2 = cur.execute("SELECT COUNT(*) FROM Harry_Styles")
            num2 = rows2.fetchone()[0]
            if num2 > num:
                limit += 1
            conn.commit()

def calculations(filename, cur, conn):
    city_dict = {}
    cur.execute("SELECT City_id.city, Harry_Styles.attendance FROM City_id JOIN Harry_Styles ON City_id.city_id == Harry_Styles.city_id")
    results = cur.fetchall()
    for result in results:
        if result[0] not in city_dict:
            city_dict[result[0]] = 0
        city_dict[result[0]] += result[1]
    f = open(filename, "w")
    f.write("Harry Styles Concert Attendance Totals Based On City\n")
    for city in city_dict:
        f.write(city+": "+str(city_dict[city])+"\n")

    cur.execute("SELECT population_data.city_id, population_data.population, Harry_Styles.attendance FROM population_data JOIN Harry_Styles ON Harry_Styles.city_id == population_data.city_id")
    results = cur.fetchall()
    f.write("\n")
    f.write("Proportion of City Population Who Attended Concert\n")
    percentages = {}
    for result in results:
        cur.execute("SELECT city FROM City_id WHERE city_id = ?", (result[0],))
        city= cur.fetchone()[0]
        percentage = round((result[2] / result[1]), 4)
        f.write(city+": "+str(percentage)+"\n")
        percentages[city] = percentage

    percent_dict = {}
    cur.execute("SELECT City_id.city, Harry_Styles.attendance, Harry_Styles.capacity FROM City_id JOIN Harry_Styles ON City_id.city_id == Harry_Styles.city_id")
    results = cur.fetchall()
    f.write("\n")
    f.write("Fullness of Venues\n")
    for result in results:
        city = result[0]
        percent = round((result[1] / result[2]), 4)
        f.write(city+": "+str(percent)+"\n")
        percent_dict[city] = percent

    score_dict = {}
    cur.execute("SELECT City_id.city, Location_scores.score, Location_scores.venue FROM City_id JOIN Location_scores ON City_id.city_id == Location_scores.city_id")
    results = cur.fetchall()
    f.write("\n")
    f.write("Popularity Scores Based on Venue\n")
    for result in results:
        city = result[0]
        score = result[1]
        venue = result[2]
        f.write(venue+": "+str(score)+"\n")
        score_dict[city] = score

    f.write("\n")
    f.write("Popularity Scores in Comparison to Fullness of Harry's Shows\n")
    for city in percent_dict:
        for city2 in score_dict:
            if city == city2:
                comparison = round((percent_dict[city] - score_dict[city]), 4)
                f.write(city+": "+str(comparison)+"\n")
    f.close()
    return city_dict

def attendance_visualization(cur, conn):
    values = calculations("calculations.txt", cur, conn)
    sorted_values = sorted(values.items(), key = lambda x: x[1], reverse=True)
    city_list = []
    attendance_list = []
    for item in sorted_values:
        if len(city_list) < 12:
            city_list.append(item[0])
            attendance_list.append(item[1])
    plt.figure()
    plt.bar(city_list, attendance_list, color = 'hotpink')
    plt.title("Harry Styles Total Concert Attendance In Top 10 Cities")
    plt.xlabel("Cities")
    plt.ylabel("Attendance")
    plt.xticks(rotation = 45)
    plt.tight_layout()
    plt.colorbar
    plt.savefig('AttendanceTotals')

def main():
    harry_data = concert_data()
    cur, conn = make_database('concerts.db')
    make_city_id_table(harry_data, cur, conn)
    make_table(harry_data, cur, conn)
    calculations("calculations.txt", cur, conn)
    attendance_visualization(cur, conn)

main()
