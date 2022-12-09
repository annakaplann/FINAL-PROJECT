import json
import os
import requests
import sqlite3
import matplotlib.pyplot as plt
import re
import sys

api_key = "Mjk2NjIyNTN8MTY2OTY3Nzg5Mi40OTk3MTM0"

def get_venue():
    url = f'https://api.seatgeek.com/2/venues?per_page=101&client_id={api_key}'
    try:
        resp = requests.get(url)
        data = json.loads(resp.text)
    except:
        return None
    venue_lst = []
    for item in data['venues']:
        venue = item['name']
        city = item['city']
        score = item['score']
        venue_lst.append((venue, city, score))
    return venue_lst

def make_database(database_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+database_name)
    cur = conn.cursor()
    return cur, conn

def make_city_id_table(data, cur, conn):
    city_list = []
    limit = 0
    for city in data:
        if city[1] not in city_list:
            city_list.append(city[1])
    cur.execute("CREATE TABLE IF NOT EXISTS City_id (city_id INTEGER PRIMARY KEY, city TEXT UNIQUE)")
    for x in range(len(city_list)):
        #print(city_list[x])
        if limit < 25:
            rows = cur.execute("SELECT COUNT(*) FROM City_id")
            num = rows.fetchone()[0]
            cur.execute("INSERT OR IGNORE INTO City_id VALUES (?, ?)", (None, city_list[x]))
            rows2 = cur.execute("SELECT COUNT(*) FROM City_id")
            num2 = rows2.fetchone()[0]
            if num2 > num:
                limit += 1
            conn.commit()

def make_location_table(data, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Location_scores (venue TEXT PRIMARY KEY, city_id INTEGER, score NUMBER)")
    limit = 0
    for concert in data:
       if limit < 25:
            venue = concert[0]
            cur.execute("SELECT city_id FROM City_id WHERE city = ?", (concert[1],))
            city_id = int(cur.fetchone()[0])
            score = concert[2]
            rows = cur.execute("SELECT COUNT(*) FROM Location_scores")
            num = rows.fetchone()[0]
            cur.execute("INSERT OR IGNORE INTO Location_scores (venue, city_id, score) values(?, ?, ?)", (venue, city_id, score))
            rows2 = cur.execute("SELECT COUNT(*) FROM Location_scores")
            num2 = rows2.fetchone()[0]
            if num2 > num:
                limit += 1
            conn.commit()
    
def make_visualization(cur, conn):
    percent_dict = {}
    cur.execute("SELECT City_id.city, Harry_Styles.attendance, Harry_Styles.capacity FROM City_id JOIN Harry_Styles ON City_id.city_id == Harry_Styles.city_id")
    results = cur.fetchall()
    for result in results:
        city = result[0]
        percent = round((result[1]/result[2]), 4)
        percent_dict[city] = percent
    score_dict = {}
    cur.execute("SELECT City_id.city, Location_scores.score, Location_scores.venue FROM City_id JOIN Location_scores ON City_id.city_id == Location_scores.city_id")
    results = cur.fetchall()
    for result in results:
        city = result[0]
        score = result[1]
        venue = result[2]
        score_dict[city] = score
    comparison_dict = {}
    for city in percent_dict:
        for city2 in score_dict:
            if city == city2:
                comparison = round((percent_dict[city] - score_dict[city]), 4)
                comparison_dict[city] = comparison
    sorted_comparisons = sorted(comparison_dict.items(), key = lambda x: x[1], reverse = True)
    city_list = []
    comparison_list = []
    for item in sorted_comparisons:
        if len(city_list) < 12:
            city_list.append(item[0])
            comparison_list.append(item[1])

    plt.figure()
    plt.bar(city_list, comparison_list, color = 'brown')
    plt.title("Popularity Scores in Comparison to Fullness of Harry's Shows")
    plt.xlabel("Cities")
    plt.ylabel("Popularity Scores Compared to Fullness of Shows")
    plt.xticks(rotation = 45)
    plt.tight_layout()
    plt.colorbar
    plt.savefig('PopularityScores')


def main():
    venue_data = get_venue()
    cur, conn = make_database("concerts.db")
    make_city_id_table(venue_data, cur, conn)
    make_location_table(venue_data, cur, conn)
    make_visualization(cur, conn)
    print("Done")
    



if __name__ == "__main__":
    main()





