# Marco Salazar
# 3/20/2019
# Attempt to collect data on Coronavirus, Covid, and Pandemic terms to correlate the data with the stock market and
# Cryptocurrencies.

import pandas as pd
import numpy as np
import io
import requests
from bs4 import BeautifulSoup
import re

import pprint
import urllib.parse
from datetime import timedelta, date
from urllib.parse import urlparse
headers={
'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}


def googleSearch(term, year, month, day):
    # //this is the actual query we are going to scrape
    url = 'https://www.google.com/search?q={}&source=lnt&tbs=cdr%3A1%2Ccd_min%3A{}%2F{}%2F{}%2Ccd_max%3A{}%2F{}%2F{}&tbm='.format(term ,month, day, year, month, day, year)
    try:
        r = requests.get(url, headers=headers)
        c = r.content
        soup = BeautifulSoup(c, 'html.parser')
        # // a is a list
        a = soup.find('div', attrs = {'id' : 'result-stats'})
        b =str(a.contents).replace(",", "")
        c = [int(s) for s in b.split() if s.isdigit()]
        results = c[0]
        return results
    except Exception as ex:
        print(ex)


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


sy = input("Enter beginning year: ")
sm = input("Enter beginning month: ")
sd = input("Enter beginning day: ")
ey = input("Enter last year: ")
em = input("Enter last month: ")
ed = input("Enter last day: ")
ed = int(ed) + 1


start_date = date(int(sy), int(sm), int(sd))
end_date = date(int(ey), int(em), int(ed))
print('date,coronavirus,covid,pandemic')
for single_date in daterange(start_date, end_date):
    a = googleSearch('coronavirus', str(single_date.year), str(single_date.month), str(single_date.day))
    b = googleSearch('covid', str(single_date.year), str(single_date.month), str(single_date.day))
    c = googleSearch('pandemic', str(single_date.year), str(single_date.month), str(single_date.day))
    print(str(single_date) + "," + str(a) + "," + str(b) + "," + str(c))
