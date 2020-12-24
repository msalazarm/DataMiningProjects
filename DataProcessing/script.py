# Marco Salazar
# 12/3/2018
# Using data that was scraped by https://www.scrapestorm.com/ from Steam,
# I processed the data to create a list of All Steam games to analyze the price point that I should release one of my
# games at.

# The file will be really big, unless you comment out any instance where  language, requirements and tags are gathered.

import pandas as pd
import numpy as np
import io
import requests
from bs4 import BeautifulSoup
import re

import pprint
data = pd.read_csv(r"./AllSteamGames_FinishedData-ScrapeStorm (1).csv")
data.head(5)

data['Price'] = data['Price'].fillna(0)
data['Discount'] = data['Discount'].fillna(0)
data['Sentiment'] = data['Sentiment'].fillna("none")
data['OS'] = data['OS'].fillna("none")

b = list(data) 
b.append('downloads')
b.append('windows')
b.append('mac')
b.append('linux')
b.append('htcvive')
b.append('oculusrift')
b.append('windowsmr')
b.append('average_length')
b.append('language')
b.append('requirements')
b.append('tags')
b[2] = 'date'
b[3] = 'price'
b[4] = 'sentiment'
b[5] = 'os'
b[6] = 'discount'
newDataframe1 = pd.DataFrame(columns = b)
newDataframe1


def whatSentiment(string):
  if string.find("Overwhelmingly Negative") != -1:
    return 1
  if string.find("Very Negative") != -1:
    return 2
  if string.find("Mostly Negative") != -1:
    return 4
  if string.find("Mostly Positive") != -1:
    return 6
  if string.find("Very Positive") != -1:
    return 8
  if string.find("Overwhelmingly Positive") != -1:
    return 9
  if string.find("Negative") != -1:
    return 3
  if string.find("Mixed") != -1:
    return 5
  if string.find("Positive") != -1:
    return 7
  return 0


def numberofdownloads(str):
  numbers = [int(s) for s in str.split() if s.isdigit()]
  if not numbers:
    return 0
  else:
    return numbers[0]


def iswindows(string):
  if string.find("win") == -1:
    return 0
  else:
    return 1


def ismac(string):
  if string.find("mac") == -1:
    return 0
  else:
    return 1


def islinux(string):
  if string.find("linux") == -1:
    return 0
  else:
    return 1


def ishtcvive(string):
  if string.find("htcvive") == -1:
    return 0
  else:
    return 1


def isoculusrift(string):
  if string.find("oculusrift") == -1:
    return 0
  else:
    return 1


def iswindowsmr(string):
  if string.find("windowsmr") == -1:
    return 0
  else:
    return 1


def averagelength(row):
  try:
    re1='.*?'	# Non-greedy match on filler
    re2='\\/'	# Uninteresting: c
    re3='.*?'	# Non-greedy match on filler
    re4='\\/'	# Uninteresting: c
    re5='.*?'	# Non-greedy match on filler
    re6='\\/'	# Uninteresting: c
    re7='.*?'	# Non-greedy match on filler
    re8='(\\/)'	# Any Single Character 1
    re9='(\\d+)'	# Integer Number 1
    re10='(\\/)'	# Any Single Character 2

    rg1 = re.compile(re1+re2+re3+re4+re5+re6+re7+re8+re9+re10,re.IGNORECASE|re.DOTALL)
    reviewurl = rg1.findall(row[1])
    reviewurl = 'https://steamcommunity.com/app/' + reviewurl[0][0] + reviewurl[0][1] + reviewurl[0][2] + 'reviews/?browsefilter=mostrecent&amp;p=1#scrollTop=0'

    r = requests.get(reviewurl)
    c = r.content
    soup = BeautifulSoup(c)
    main_content = soup.findAll('div', attrs = {'class' : 'hours'})
    re1='.*?'	# Non-greedy match on filler
    re3='([+-]?\\d*\\.\\d+)(?![-+0-9\\.])'	# Float 1
    re4='(\\s+)'	# White Space 1

    rg2 = re.compile(re1+re3+re4,re.IGNORECASE|re.DOTALL)
    str = ''
    for i in main_content:
      str = str + ''.join(i)
    hours = rg2.findall(str)
    average = 0
    count = 0
    for i in hours:
      average = float(i[0]) + average
      count = count +1
    if count != 0:
      average = average*1.0/count
    return average
  except KeyboardInterrupt:
    raise Exception('')
  except:
    return 0


def checkreviews(newrow, soup):
  try:
    html = soup.find('div', attrs = {'class' : 'subtitle column all'})

    re1='.*?'	# Non-greedy match on filler
    re2='(\\(.*\\))'	# Round Braces 1

    rg = re.compile(re1+re2,re.IGNORECASE|re.DOTALL)
    string = str(html.find_next_sibling("div"))
    string = string.replace(",", "")
    reviews = 0
    reviews = re.search(r'\d+', string).group()
    reviews = int(reviews)
    return reviews if reviews > newrow[7] else newrow[7]
  except AttributeError:
    return newrow[7]
  except KeyboardInterrupt:
    raise Exception('')


def getlanguage(newrow, soup):
  try:
    html = soup.find('table', attrs = {'class' : 'game_language_options'})
    return str(html)
  except AttributeError:
    return "none"
  except KeyboardInterrupt:
    raise Exception('')


def getrequirements(newrow, soup):
  try:
    html = soup.find('div', attrs = {'class' : 'sysreq_contents'})
    return str(html)
  except AttributeError:
    return "none"
  except KeyboardInterrupt:
    raise Exception('')


def gettags(newrow, soup):
  try:
    html = soup.find('div', attrs = {'class' : 'glance_tags popular_tags'})
    return str(html)
  except AttributeError:
    return "none"
  except KeyboardInterrupt:
    raise Exception('')


def validate(newrow, oldrow):
  try:
    r = requests.get(oldrow[1])
    c = r.content
    soup = BeautifulSoup(c)
#     review_html = soup.find('div', attrs = {'class' : 'subtitle column all'})
    newrow[7] = checkreviews(newrow, soup)
    newrow.append(getlanguage(newrow, soup))
    newrow.append(getrequirements(newrow, soup))
    newrow.append(gettags(newrow, soup))
    return newrow
  except KeyboardInterrupt:
    raise Exception('')


def cleanRow(row):
  newrow = [row[0], row[1], row[2], row[3]]
  newrow.append(whatSentiment(row[4]))
  newrow.append(row[5])
  newrow.append(row[6])
  newrow.append(numberofdownloads(row[4]))
  newrow.append(iswindows(row[5]))
  newrow.append(ismac(row[5]))
  newrow.append(islinux(row[5]))
  newrow.append(ishtcvive(row[5]))
  newrow.append(isoculusrift(row[5]))
  newrow.append(iswindowsmr(row[5]))
  newrow.append(averagelength(row))
  newrow = validate(newrow, row)
  global cleaned 
  cleaned = cleaned +1
  print(str(cleaned) + '/' + str(total)+ " :      " + str((float(cleaned/total*100))) + "%")
  return newrow


def cleanData(dataframe):
  newDataframe = pd.DataFrame(columns = b)
  for index, row in dataframe.iterrows():
    newDataframe.loc[len(newDataframe)] = cleanRow(row)
  newDataframe = newDataframe.drop('os', 1)
  return newDataframe


cleaned = 0
total = len(data)
newdataframe = cleanData(data)
newdataframe.head(5)

newdataframe.to_csv(r"./temp/AllSteamGames.csv")
