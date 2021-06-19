from bs4 import BeautifulSoup 
import requests 
def getHTML(url): 
    response = requests.get(url) 
    return response.text
url = "https://en.wikipedia.org/wiki/Public_holidays_in_the_United_States"
html = getHTML("https://en.wikipedia.org/wiki/Public_holidays_in_the_United_States")

response = requests.get(url) 
print(response.status_code)

def getDate(date):
    month = date[0]
    year = 2021
    day = date[1]

    if month == 'January':
        month = 1
    elif month == 'February':
        month = 2
    elif month == 'March':
        month = 3
    elif month == 'April':
        month = 4
    elif month == 'May':
        month = 5
    elif month == 'June':
        month = 6
    elif month == 'July':
        month = 7
    elif month == 'August':
        month = 8
    elif month == 'September':
        month = 9
    elif month == 'October':
        month = 10
    elif month == 'November':
        month = 11
    elif month == 'December':
        month = 12

    return f'{year}-{month}-{day}'

# Parse
soup = BeautifulSoup(html,'html.parser')
table = soup.find('table',attrs = {'class':'wikitable'})
holidays = list()
for row in table.find_all_next('tr'): 
    cells = row.find_all_next('td')
    #print(cells)
    try:
        holiday = {} 
        exists = False
        holiday['name'] = cells[2].text
        preformatted_date = cells[1].find('span').text.split(' ')
        if len(preformatted_date) == 2:
            holiday['date'] = getDate(preformatted_date)
        for h in holidays:
            if h['name'] == holiday['name']:
                exists = True
        if holiday['date'] != None and not exists:
            holidays.append(holiday)
    except:
        continue

tables = soup.find_all('table', attrs={'class':'wikitable'})
for table in tables:
    for row in table.find_all_next('tr'): 
        cells = row.find_all_next('td')
        #print(cells[0])
        try:
            holiday = {} 
            exists = False
            holiday['name'] = cells[1].text
            preformatted_date = cells[0].text.split(' ')
            if len(preformatted_date) == 2:
                holiday['date'] = getDate(preformatted_date)
            for h in holidays:
                if h['name'] == holiday['name']:
                    exists = True
            if holiday['date'] != None and not exists:
                holidays.append(holiday)
        except:
            continue

print(holidays)