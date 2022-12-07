import os
import sqlite3
import matplotlib.pyplot as plt

def make_database(database_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+database_name)
    cur = conn.cursor()
    return cur, conn

def attendance_calculations(filename, cur, conn):

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
    return city_dict

def percentage_calculations(filename, cur, conn):
    cur.execute("SELECT population_data.city, population_data.population, Harry_Styles.attendance FROM population_data JOIN Harry_Styles ON Harry_Styles.city == population_data.city")
    results = cur.fetchall()
    f = open(filename, "w")
    f.write("\n")
    f.write("Proportion of City Population Who Attended Concert\n")
    percentages = {}
    for result in results:
        city = result[0]
        percentage = round((result[2] / result[1]), 4)
        f.write(city+": "+str(percentage)+"\n")
        percentages[city] = percentage
    f.close()
    return percentages

def score_calculations(filename, cur, conn):

    #WORKING ON THIS: We want to subtract the scores from the percentages based on city
    f = open(filename, "w")
    percent_dict = {}
    cur.execute("SELECT city, attendance, capacity FROM Harry_Styles")
    results = cur.fetchall()
    f.write("\n")
    f.write("Fullness of Venues\n")
    for result in results:
        city = result[0]
        percent = round((result[1] / result[2]), 4)
        f.write(city+": "+str(percent)+"\n")
        percent_dict[city] = percent

    score_dict = {}
    cur.execute("SELECT Location_scores.city, Location_scores.score, Venue_id.venue FROM Location_scores JOIN Venue_id ON Location_scores.venue_id == Venue_id.venue_id")
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
    f.write("Popularity Scores in Comparison to Attendance\n")
    print(percent_dict)
    print(score_dict)
    f.close()

    
'''
def visualizations(cur, conn):

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
    plt.savefig("Attendance")


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
    plt.title("Proportion of Concert Attendance by City Population")
    plt.xlabel("Cities")
    plt.ylabel("Proportion")
    plt.xticks(rotation = 45)
    plt.tight_layout()
    plt.colorbar
    plt.savefig('PercentCalculations')
'''

def main():
    cur, conn = make_database('concerts.db')
    attendance_calculations("calculations.txt", cur, conn)
    percentage_calculations("calculations.txt", cur, conn)
    score_calculations("calculations.txt", cur, conn)



