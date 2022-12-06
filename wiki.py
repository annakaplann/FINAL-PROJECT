from bs4 import BeautifulSoup
import os
import re
import requests
import sqlite3

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

def make_table(data, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Harry_Styles (date TEXT PRIMARY KEY, city TEXT, attendance INTEGER, capacity INTEGER)")
    limit = 0
    for concert in data:
        if limit < 25:
            date = concert[0]
            city = concert[1]
            attendance = concert[2]
            capacity = concert[3]
            rows = cur.execute("SELECT COUNT(*) FROM Harry_Styles")
            num = rows.fetchone()[0]
            cur.execute("INSERT OR IGNORE INTO Harry_Styles (date, city, attendance, capacity) VALUES (?, ?, ?, ?)", (date, city, attendance, capacity))
            rows2 = cur.execute("SELECT COUNT(*) FROM Harry_Styles")
            num2 = rows2.fetchone()[0]
            if num2 > num:
                limit += 1
            conn.commit()

def calculations(filename, cur, conn):
    city_dict = {}
    cur.execute("SELECT city, attendance FROM Harry_Styles")
    results = cur.fetchall()
    for result in results:
        if result[0] not in city_dict:
            city_dict[result[0]] = 0
        city_dict[result[0]] += result[1]
    f = open(filename, "w")
    f.write("Harry Styles Concert Attendance Totals Based On City\n")
    for city in city_dict:
        f.write(city+": "+str(city_dict[city])+"\n")
    f.close()

def main():
    harry_data = concert_data()
    cur, conn = make_database('concerts.db')
    make_table(harry_data, cur, conn)
    calculations("calculations.txt", cur, conn)
    file = open("calculations.txt", "r")
    print(file.read())
    file.close()

main()
