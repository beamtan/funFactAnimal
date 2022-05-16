from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
# to csv file
import csv
from datetime import datetime

def write_to_csv(data):
    with open('webScraping/funfactAnimal.csv', 'a', newline='', encoding='utf-8') as file:
        fileWriter = csv.writer(file)
        fileWriter.writerow(data)

def getAnimalName():
    nameList = []
    keep = {}
    url = 'https://a-z-animals.com/animals/'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()

    data = BeautifulSoup(webpage, 'html.parser')
    animalList = data.find_all('li', {'class':'list-item col-md-4 col-sm-6'})
    for i in animalList:
        # print(i)
        name = i.find_next_sibling()
        if name:
            nameList.append(name.text)
    properList = [x.replace(' ', '-') for x in nameList]
    return properList

def getData():
    keep = {}
    aList = getAnimalName()
    for i, name in enumerate(aList):
        try:
            url = 'https://a-z-animals.com/animals/{}/'.format(name)
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            data = BeautifulSoup(webpage, 'html.parser')
            funfact = data.find('p', {'class': 'mb-0'})
            if funfact and not funfact == (None,''):
                funfact = funfact.text
                keep[name] = funfact
            else:
                keep[name] = 'no data'
            print('{} {}: {} is saved'.format(i, name, funfact))
        except:
            continue
    for index, name in enumerate(keep.items(), 1):
        data = [index, name[0], name[1]]
        write_to_csv(data)

getData()

