import csv
import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver

quote_page = 'http://www.yad2.co.il/Cars/Car.php?AreaID=&City=&HomeTypeID=&Page='

phantomjs_path = "C:\Python27\misc\phantomjs-2.1.1-windows\\bin\phantomjs.exe"

browser = webdriver.PhantomJS(executable_path=phantomjs_path, service_log_path=os.path.devnull)
index = 1

data = [['carMake', 'carModel', 'engine', 'year', 'price', 'owners', 'gear', 'location', 'date']]

while index < 100:
    browser.get(quote_page + str(index))

    # fucking yad2
    time.sleep(5)

    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('table', attrs={'class': 'main_table'})
    body = table.find('tbody')
    rows = body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip().encode("UTF-8") for ele in cols]
        if len(cols) > 3 and any(c for c in cols if "window" not in c):
            car = cols[4].split(" - ")

            carMake = car[0]
            carModel = car[1]
            engine = cols[6]
            year = cols[8]
            price = cols[10]
            owners = cols[12]
            gear = cols[14]
            location = cols[16]
            date = cols[20]

            row = [carMake, carModel, engine, year, price, owners, gear, location, date]

            data.append(row)

    with open("C:\Users\ilial\Desktop\index.csv", "w+") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(data)

    index = index + 1
    print index
