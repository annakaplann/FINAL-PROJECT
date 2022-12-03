from bs4 import BeautifulSoup
import os
import re
import requests
import sqlite3
import matplotlib

def concert_data():

    resp = requests.get('https://en.wikipedia.org/wiki/Love_On_Tour')
    soup = BeautifulSoup(resp.text, 'html.parser')
    table_tags = soup.find_all('table', class_ = 'wikitable plainrowheaders')

    #HARRY STYLES LOVE ON TOUR 2021 & 2022
    for table in table_tags:
        for concert in table.find_all('tr'):
            concert_info = concert.find_all('td')
            if concert_info != []:
                city = concert_info[0].text.strip()
                pattern = "(\d*,\d*) / .*"
                tickets = concert_info[-2].text.strip()
                tickets_sold = re.findall(pattern, tickets)
                pattern2 = ".* / (\d*,\d*)"
                capacity = re.findall(pattern2, tickets)
                if tickets_sold != []:
                    number = re.sub(",", "", tickets_sold[0])
                    number2 = re.sub(",", "", capacity[0])
                    print([city, int(number), int(number2)])

    resp2 = requests.get('https://en.wikipedia.org/wiki/Harry_Styles:_Live_on_Tour')
    soup = BeautifulSoup(resp2.text, 'html.parser')
    table_tags2 = soup.find_all('table', class_ = 'wikitable')

    #HARRY STYLES LIVE ON TOUR 2017 & 2018
    for table in table_tags2:
        for concert in table.find_all('tr'):
            concert_info = concert.find_all('td')
            if len(concert_info) >= 5 and len(concert_info) <= 7:
                city = concert_info[1].text.strip()
                pattern = "(\d*,\d*) / .*"
                tickets = concert_info[-2].text.strip()
                tickets_sold = re.findall(pattern, tickets)
                pattern2 = ".* / (\d*,\d*)"
                capacity = re.findall(pattern2, tickets)
                if tickets_sold != []:
                    number = re.sub(",", "", tickets_sold[0])
                    number2 = re.sub(",", "", capacity[0])
                    print([city, int(number), int(number2)])
    
concert_data()
