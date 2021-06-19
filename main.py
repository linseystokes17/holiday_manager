# Plan of Attack
    # 1. Use Command line to run 'python main.py'
        # 1. Load holidays.json and save to dictionary
        # 2. scrape public holidays from wikipedia and save
    # 2. Print 'Holiday Management, {numberHolidays}' screen
    # 3. While not exit: print menu and get input
        # 1. Add a Holiday
        # 2. Remove a Holiday
        # 3. Save Holiday List
        # 4. View Holidays
        # 5. Exit
    # 4. show screen of input option
from dataclasses import dataclass, field
import json
from bs4 import BeautifulSoup
import requests 
import datetime

# ---------------- Web Scraping Setup ------------------
def getHTML(url): 
    response = requests.get(url) 
    return response.text
url = "https://en.wikipedia.org/wiki/Public_holidays_in_the_United_States"
html = getHTML("https://en.wikipedia.org/wiki/Public_holidays_in_the_United_States")

response = requests.get(url) 
print(response.status_code)
soup = BeautifulSoup(html,'html.parser')

# Web scraping utility function (format dates)
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
    
    if len(day)>2:
        return None

    return f'{year}-{month}-{day}'

def getWikipedia():
    # get first table (formatted differently)
    table = soup.find('table',attrs = {'class':'wikitable'})
    for row in table.find_all_next('tr'): 
        cells = row.find_all_next('td')
        try:
            holiday = {} 
            exists = False
            holiday['name'] = cells[2].text
            preformatted_date = cells[1].find('span').text.split(' ')
            if len(preformatted_date) == 2:
                holiday['date'] = getDate(preformatted_date)
            for h in holidays:
                    if h.name == holiday['name']:
                        exists = True
            if holiday['date'] != None and not exists:
                h = Holiday(holiday['name'], holiday['date'])
                holidays.append(h)
        except:
            break

    # get rest of tables
    tables = soup.find_all('table', attrs={'class':'wikitable'})
    for table in tables:
        for row in table.find_all_next('tr'): 
            cells = row.find_all_next('td')
            try:
                holiday = {} 
                exists = False
                holiday['name'] = cells[1].text
                preformatted_date = cells[0].text.split(' ')
                if len(preformatted_date) == 2:
                    holiday['date'] = getDate(preformatted_date)
                for h in holidays:
                    if h.name == holiday['name']:
                        exists = True
                if holiday['date'] != None and not exists:
                    h = Holiday(holiday['name'], holiday['date'])
                    holidays.append(h)
            except:
                continue

# ----------------- menu functions ------------------------
# add holiday menu
def addHolidayMenu():
    print('Add a Holiday\n==========')
    holidayName = input('Holiday Name: ')
    date = input(f'Date: ')
    message = addHoliday(holidayName, date)
    if not message:
        print(f'\nError: \nInvalid date. Please try again')
    else:
        print(f'\nSuccess:\n{holidayName} ({date}) has been added to the holiday list')

# view holidays menu
def viewHolidaysMenu():
    print('View Holidays\n==========')
    year = input('Which year?: ')
    week = input('Which week? #[1-52, Leave blank for current week]: ')
    if week=='':
        viewHolidays(year)
    else:
        viewHolidays(year, week)

# ------------------- actual menu functionality --------------------
# add holiday to list and check date functionality
def addHoliday(name, date):
    date_list = date.split('-')
    if len(date_list[0]) == 4 and len(date_list[1]) == 2 and int(date_list[1]) > 0 and int(date_list[1]) <= 12 and len(date_list[2])==2:
        h = Holiday(name, date)
        holidays.append(h)
        return True
    return False

# function to check week and year args from menu and call getHolidays
def viewHolidays(*args):
    if len(args) == 2:
        week = int(args[1])
        year = int(args[0])
        print(f'\nThese are the holidays for {year} week #{week}')
        getHolidays(week, year,False)
    else:
        year = int(args[0])
        week = 2
        weatherValue = input('Would you like to see this week\'s weather? [y/n]: ')
        
        if weatherValue == 'y':
            weather = True
            print(f'\nThese are the holidays for this week:')
            getHolidays(week, year, True)

        else:
            weather = False
            print(f'\nThese are the holidays for this week:')
            getHolidays(week, year,False)

# function to return list of holidays based on weekNum, year, and weather (T/F)
# technical requirements says use lambda expressions - TODO
def getHolidays(*args):
    week = args[0]
    year = args[1]
    weather = args[2]
    for holiday in holidays:
        date_split = holiday.date.split('-')
        weekNum = datetime.date(int(holiday.date.split('-')[0]), int(holiday.date.split('-')[1]), int(holiday.date.split('-')[2])).isocalendar()[1]
        if not weather:
            if year == int(date_split[0]) and week == weekNum:
                print(holiday)
        # TODO - call weather API for date if True

# -------------------- intialize dataclass -----------------------
@dataclass
class Holiday:
    name: str
    date: str # "2021-01-12"

    def __str__(self):
        return f'{self.name} ({self.date})'

# create list of dictionaries (have a name and date)
holidays = list()

# --------------------------- load json file ------------------------
# load holidays from json file
with open('holidays.json') as json_file:
    data = json.load(json_file)
    for i in range(len(data['holidays'])):
        # add holiday as dataclass Holiday object
        holiday = data['holidays'][i]
        h = Holiday(holiday['name'], holiday['date'])
        holidays.append(h)

# ---------------------------- load beautifulsoup scraping -------------------
# load holidays from wikipedia with webscraping
getWikipedia()

# ------------------------- printing / menu ---------------------------
print('Holiday Management \n ===================')
print(f'There are {len(holidays)} holidays stored in the system.')

# while exit has not been confirmed, keep printing menu options
exit = False
while not exit:
    # print menu options
    print('\n\nHoliday Menu\n================')
    print('1. Add a Holiday')
    print('2. Remove a Holiday')
    print('3. Save Holiday List')
    print('4. View Holidays')
    print('5. Exit')
    selection = int(input('Enter the number of the menu option you want '))
    print('\n\n')
    # if exit
    if selection == 5:
        print('Exit\n=====')
        confirm = input('Are you sure you want to exit? [y/n] ')
        if confirm == 'y':
            print('\nGoodbye!')
            exit = True
    elif selection == 1:
        addHolidayMenu()
    elif selection == 2:
        print('Remove a Holiday\n==========')
    elif selection == 3:
        print('Saving Holiday List\n==========')
    elif selection == 4:
        viewHolidaysMenu()
            
