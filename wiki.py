from bs4 import BeautifulSoup
import os
import re
import requests
import sqlite3
import matplotlib

#API_KEY = 'qub1dkZGsM84AARLJmkdtimD909X0r0k'

def concert_data():
    resp = requests.get('https://en.wikipedia.org/wiki/Love_On_Tour')
    soup = BeautifulSoup(resp.text, 'html.parser')
    table_tags = soup.find_all('table', class_ = 'wikitable plainrowheaders')
    table1 = table_tags[0]
    table2 = table_tags[2]

    #HARRY STYLES NORTH AMERICAN SHOWS 2021
    for concert in table1.find_all('tr'):
        concert_info = concert.find_all('td')
        if concert_info != []:
            city = concert_info[0].text.strip()
            pattern = "(\d*,\d*) / .*"
            tickets = concert_info[-2].text.strip()
            tickets_sold = re.findall(pattern, tickets)
            if tickets_sold != []:
                number = re.sub(",", "", tickets_sold[0])
                print([city, int(number)])

    #HARRY STYLES NORTH AMERICAN SHOWS 2022
    for concert in table2.find_all('tr'):
        concert_info = concert.find_all('td')
        if concert_info != []:
            city = concert_info[0].text.strip()
            pattern = "(\d*,\d*) / .*"
            tickets = concert_info[-2].text.strip()
            tickets_sold = re.findall(pattern, tickets)
            if tickets_sold != []:
                number = re.sub(",", "", tickets_sold[0])
                print([city, int(number)])
    
    '''
    for table in table_tags:
        tr_tags = table.find_all('tr')
        for tr in tr_tags:
            td_tags = tr.find_all('td')
            print(td_tags)
            #for td in td_tags:
                #print(td)

    captions = soup.find_all("caption")
    for caption in captions:
        if caption.text == "List of North American concerts":
'''

            #city = td_tags[0].text.strip()
            #print(city)
            #a_tag = td_tag.find('a')
            #print(a_tag)
            #print(td_tag.text)
                #city = td.text
                #print(city)

concert_data()

    #base_url = 'https://app.ticketmaster.com/discovery/v2/'
    #harry_styles = 'K8vZ9174XZ0'
    #harry_url = f'https://app.ticketmaster.com/discovery/v2/events.json?attractionId={harry_styles}&countryCode=US&apikey={API_KEY}'

