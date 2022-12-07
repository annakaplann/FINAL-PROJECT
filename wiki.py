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


def percent_calculations(filename, cur, conn):
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
    
    cur.execute("SELECT population_data.city, population_data.population, Harry_Styles.attendance FROM population_data JOIN Harry_Styles ON Harry_Styles.city == population_data.city")
    results = cur.fetchall()
    f.write("\n")
    f.write("Percentage of City Population Who Attended Concert\n")
    percentages = {}
    for result in results:
        city = result[0]
        percentage = round((result[2] / result[1]), 4)
        print(percentage)
        print(result[1])
        f.write(city+": "+str(percentage)+"\n")
        percentages[city] = percentage
    return percentages



def calculations(filename, cur, conn):

    #WORKING ON THIS: We want to subtract the scores from the percentages based on city
    f = open(filename, "w")
    percent_lst = []
    cur.execute("SELECT city, attendance, capacity FROM Harry_Styles")
    results = cur.fetchall()
    f.write("\n")
    f.write("Fullness of Venues\n")
    for result in results:
        city = result[0]
        percent = round((result[1] / result[2]), 4)
        f.write(city+": "+str(percent)+"\n")
        percent_lst.append(percent)

    cur.execute("SELECT Location_scores.city, Location_scores.score, Venue_id.venue FROM Location_scores JOIN Venue_id ON Location_scores.venue_id == Venue_id.venue_id")
    results = cur.fetchall()
    f.write("\n")
    f.write("Popularity Scores Based on Venue\n")
    for result in results:
        city = result[0]
        venue = result[2]
        score = result[1]
        f.write(venue+": "+str(score)+"\n")

    cur.execute("SELECT city, score FROM Location_scores")
    results = cur.fetchall()
    f.write("\n")
    f.write("Popularity Scores in Comparison to Attendance\n")
    for result in results:
        city = result[0]
        score = result[1]
    f.close()

def visualization(cur, conn):
    cur.execute("SELECT city, attendance FROM Harry_Styles")
    data = cur.fetchall()
    data2 = sorted(data, key = lambda x: x[1], reverse=True)
    conn.commit()
    
    city_list = []
    attendance_list = []
    for item in data2:
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
    plt.show()



def main():
    harry_data = concert_data()
    cur, conn = make_database('concerts.db')
    make_table(harry_data, cur, conn)
    calculations("calculations.txt", cur, conn)
    percent_calculations("calculations.txt", cur, conn)
    file = open("calculations.txt", "r")
    file.close()
    visualization(cur, conn)

main()
