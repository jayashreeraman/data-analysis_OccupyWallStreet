import urllib.request
from bs4 import BeautifulSoup
import requests
import re
import ows_module
import datetime
import dateutil.parser, datetime
import xlwt

#############################################################################################################
#   This function scrapes data from Wikipedia about the Occupy Wall Street movement that
#   occurred in 2011 to get an understanding of the types of people who participated and their impact,
#   as part of an analytics project
#
#   Created by: Jayashree Raman
#   Created in: February 2017
#############################################################################################################


wikiLink = "https://en.wikipedia.org/wiki/List_of_Occupy_movement_protest_locations_in_the_United_States"
californiaLink = "https://en.wikipedia.org/wiki/List_of_Occupy_movement_protest_locations_in_California"
cityDict={}

def parse_date(d):
    #print(d)
    try:
        if d !=None or d != ' ':
            x = dateutil.parser.parse(d)
            x = datetime.datetime.strftime(x, '%d-%m-%Y')

    except:
        return d
        
    
    return x

def get_data_from_wikiTable(linkObj, stateName=''):
    
    state = ''
    city = ''
    date = ''
    refNum = ''
    index = 1
    page = requests.get(linkObj)
    soup= BeautifulSoup(page.content, 'html5lib')

    table = soup.find('table', attrs= {'class': ['wikitable', 'sortable']})
    print(table.attrs)

################################        Create an instance of ows object     ################################ 
    ows = ows_module.OccupyWallStreet
    for row in table.find_all("tr"):
        cells = row.find_all("td")

    ##    for cell in cells:
    ##        print(cell.text)
        #print(len(cells))

        if len(cells)==6:
            start_index = 1
            state = cells[0].find(text=True)
            city = cells[start_index].find(text=True)
            date = cells[start_index + 1].find(text=True)
            refNum = cells[start_index + 3].find(text=True)

    ##        newEntry = ows(state, city, date, refNum)
    ##        cityDict[city] = newEntry
            
        if len(cells)==5:
            city = cells[0].find(text=True)
            date = cells[1].find(text=True)
            refNum = cells[3].find(text=True)

        if date == None and refNum != None:
            #Code to retrieve Citation ID
            for link in soup.findAll('a', href=True, text=refNum):
                #print(link['href'])
                citationId = link['href'].replace('#','')
            #print(citationId)
            if city == "Alameda":
                citationId = "cite_note-Alameda-1"

##############################################################################################################################################################
            #Code to extract citation text
            citation = soup.find('li', {'id':citationId})
            #print(city + str(citation))
            if citation != None:
                #d = re.findall(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d\d,\s\d{4}', str(citation))
                d = re.findall(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d+,', str(citation))
                if d != []:
                    date = ''.join(d[0])+' 2011'
                elif citation != None and stateName =='California':
                    #print(str(citation))
                    d = re.findall(r'(\d\d\d\d-\d\d-\d\d)', str(citation))

                    if d != []:
                        date = ''.join(d[0])
                    #print(date)
##############################################################################################################################################################
        #print(state)
##        if stateName != ' ':
##            oState = stateName
##        print(state)
        newEntry = ows(state, city, parse_date(date), refNum)
        if stateName == 'California':
            newEntry = ows(stateName, city, parse_date(date), refNum)
        
        cityDict[index] = newEntry
        index+=1


def write_data_to_excel(dict1):
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("OWS_Wikipedia_Data", cell_overwrite_ok=True)

    sheet1.write(0, 0, "Sr Num")
    sheet1.write(0, 1, "State")
    sheet1.write(0, 2, "City")
    sheet1.write(0, 3, "Date")
    
    
    rowNum=1
    for i in range(1, len(dict1)):
        x = dict1[i]
        if x.city != '':
            sheet1.write(rowNum, 1, x.state)
            sheet1.write(rowNum, 2, x.city)
            sheet1.write(rowNum, 3, x.date)
            sheet1.write(rowNum, 0, i-1)
            rowNum += 1

    book.save("C:/Users/Jayashree RAMAN/Documents/OccupyWallStreet_DataAnalysis/OWS_Wiki_Data.xls")
    print("Excel Saved!")


get_data_from_wikiTable(wikiLink)
get_data_from_wikiTable(californiaLink, "California")
write_data_to_excel(cityDict)
