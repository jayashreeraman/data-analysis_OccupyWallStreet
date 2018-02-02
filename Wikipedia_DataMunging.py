import urllib.request
from bs4 import BeautifulSoup
import requests
import re
import ows_module
import datetime
import dateutil.parser, datetime
import xlwt

#############################################################################################
#   This function scrapes data from Wikipedia about the Occupy Wall Street movement that
#   occurred in 2011 to get an understanding of the types of people who participated and their impact,
#   as part of an analytics project
#
#   Created by: Jayashree Raman
#   Created in: February 2017
#############################################################################################


wikiLink = "https://en.wikipedia.org/wiki/List_of_Occupy_movement_protest_locations_in_the_United_States"
cityDict={}
state = ''
city = ''
date = ''
refNum = ''

page = requests.get(wikiLink)
soup= BeautifulSoup(page.content, 'html5lib')

table = soup.find('table', attrs= {'class': ['wikitable', 'sortable']})
print(table.attrs)




def parse_date(d):
    print(d)
    try:
        if d !=None or d != ' ':
            x = dateutil.parser.parse(d)
            x = datetime.datetime.strftime(x, '%d-%m-%Y')

    except:
        return d
        
    
    return x
    
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
        citationId = "cite_note-" + city.replace(' ', '_') + "-" + (refNum.replace('[', '')).replace( ']', '')
        if city == 'Kenai':
            citationId = 'cite_note-Kenai2-13'
        #print(citationId)
        citation = soup.find('li', {'id':citationId})
        #print(city + str(citation))
        if citation != None:
            d = re.findall(r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|October|November|Dec)\s\d\d,\s\d{4}', str(citation))
            if d != []:
                date = ''.join(d[0])
            #print(date)

    newEntry = ows(state, city, parse_date(date), refNum)
    cityDict[city] = newEntry

def parse_date_to_set_format(cDict):
    for key in cDict:
        x = cDict[key]
        print(x.date + x.city)
        tempDate = x.date
        if not(tempDate==None) or not(tempDate == ' '):
            x.date = parse_date(tempDate)
    

def write_data_to_excel(dict1):
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Sheet 1", cell_overwrite_ok=True)
    rowNum=1
    for key in dict1:
        x = dict1[key]
        sheet1.write(rowNum, 0, x.state)
        sheet1.write(rowNum, 1, x.city)
        sheet1.write(rowNum, 2, x.date)
        rowNum += 1

    book.save("C:/Users/Jayashree RAMAN/Documents/OccupyWallStreet_DataAnalysis/trial.xls")

write_data_to_excel(cityDict)
