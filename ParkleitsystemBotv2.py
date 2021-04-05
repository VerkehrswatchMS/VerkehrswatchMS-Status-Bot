#!/usr/bin/env python3.7

import sys
import requests
import random
import twitter
import BotConfig as config
from bs4 import BeautifulSoup

def sendTweet (msg):    
    api = twitter.Api(consumer_key=config.ckey,
                  consumer_secret=config.csecret,
                  access_token_key=config.atoken,
                  access_token_secret=config.atsecret)    
    api.PostUpdate(status=msg)

def getRandomNumber (min, max):
    value = max-min
    result = round(min+value*random.random(),0)
    return int(result)

def getComparisson(freeSpots):
    spotSize = 12.5
    totalArea = freeSpots * spotSize
    comparissons = []
    icehockeyfield = [1800, 'Eishockey-Spielfelder', 1]
    comparissons.append(icehockeyfield)
    soccerfield = [7140 , 'Fußball-Spielfelder', 1]
    comparissons.append(soccerfield)
    soccerfield = [8000 , 'mal die Fläche des Empfangsgebäudes des HBF-MS', 1]
    comparissons.append(soccerfield)
    promenadenring = [1330000, 'mal die Innenfläche des Promenadenring', 3]
    comparissons.append(promenadenring)
    bikespots = [2, 'Fahrradabstellplätze', 0]
    comparissons.append(bikespots)
    
    comparrisonCount = getRandomNumber(0,len(comparissons)-1)
    singleComp = comparissons[comparrisonCount]
    factor = round(totalArea/int(singleComp[0]),singleComp[2])
    text = singleComp[1]
    return [totalArea, factor, text]

def getFreeAndTotalNumber():
    i = 0
    freeTotal = 0
    totalSpots = 0
    generalResult = requests.get('https://www.stadt-muenster.de/tiefbauamt/parkleitsystem')
    generalSoup = BeautifulSoup(generalResult.text, 'html.parser')
    trInGeneralSoup = generalSoup.find_all('tr')    
    # connect with website
    while i<16:
        i = i+1
        statusNotFree = trInGeneralSoup[i].find("td",class_="status notFree")
        detailurl2=(trInGeneralSoup[i].find('a'))['href']
        if statusNotFree != None:
            statusNotFree = statusNotFree.text
        if statusNotFree != 'geschlossen':
            detailurl = 'https://www.stadt-muenster.de/'+detailurl2+'.html'
            result = requests.get(detailurl)        
            if result.status_code != 200:
                print("Request failed with status code: {:d}!".format(result.status_code), file=sys.stderr)            
            else:
                # get parking table
                soup = BeautifulSoup(result.text, 'html.parser')
                parking_table = soup.find('div', id='parkingStatus')
                numbers = parking_table.find_all('strong')
                free=numbers[0].text.strip()
                total=numbers[1].text.strip()
                freeTotal = freeTotal + int(free)
                totalSpots = totalSpots + int (total)
    return [freeTotal, totalSpots]



def main():    
    numbers = getFreeAndTotalNumber()
    comp = getComparisson(numbers[0])
    message = 'In #Münster werden aktuell {} von {} Autoparkplätzen in der Innenstadt nicht genutzt. Das ist eine Flächenverschwendung von {} m² (ca. {} {}). #autostadt #msVerkehr'.format(numbers[0],numbers[1], comp[0], comp[1], comp[2])
    print(message)
    #sendTweet(message)
    
if __name__ == "__main__":    
    main()


