from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

import mysql.connector
import threading
import schedule

from random import randint
import time
import config

NUMBER_OF_THREADS = 9

from scrape import TGD, FPT, PVU, TPR

driver = []
for i in range(NUMBER_OF_THREADS):
    driver.append(webdriver.Chrome(service=Service(ChromeDriverManager().install())))

dataset = {}
dataset['Laptop'] = set([])
dataset['PC'] = set([])
dataset['Screen'] = set([])
dataset['Mouse'] = set([])
dataset['Keyboard'] = set([])

def scrapeTGD0():
    TGD.LaptopScraper(driver[0], dataset['Laptop'], 'https://www.thegioididong.com/laptop/')
def scrapeTGD1():
    TGD.PCScraper(driver[1], dataset['PC'], 'https://www.thegioididong.com/may-tinh-de-ban/')
def scrapeTGD2():
    TGD.ScreenScraper(driver[2], dataset['Screen'], 'https://www.thegioididong.com/man-hinh-may-tinh/')
    TGD.Scraper(driver[2], dataset['Mouse'], 'https://www.thegioididong.com/chuot-may-tinh/')
    TGD.Scraper(driver[2], dataset['Keyboard'], 'https://www.thegioididong.com/ban-phim/')
def scrapeFPT0():
    FPT.LaptopScraper(driver[3], dataset['Laptop'], 'https://fptshop.com.vn/may-tinh-xach-tay/')
def scrapeFPT1():
    FPT.PCScraper(driver[4], dataset['PC'], 'https://fptshop.com.vn/may-tinh-de-ban/')
    FPT.ScreenScraper(driver[4], dataset['Screen'], 'https://fptshop.com.vn/man-hinh/')
    FPT.Scraper(driver[4], dataset['Mouse'], 'https://fptshop.com.vn/phu-kien/chuot/')
    FPT.Scraper(driver[4], dataset['Keyboard'], 'https://fptshop.com.vn/phu-kien/ban-phim/')
def scrapeTPR0():
    TPR.Scraper(driver[5], dataset['Mouse'], 'https://thinkpro.vn/chuot')
    TPR.Scraper(driver[5], dataset['Keyboard'], 'https://thinkpro.vn/ban-phim')
    TPR.LaptopScraper(driver[5], dataset['Laptop'], 'https://thinkpro.vn/laptop')
def scrapePVU0():
    PVU.LaptopScraper(driver[6], dataset['Laptop'], 'https://phongvu.vn/c/laptop/')
def scrapePVU1():
    PVU.ScreenScraper(driver[7], dataset['Screen'], 'https://phongvu.vn/c/man-hinh-may-tinh/')
def scrapePVU2():
    PVU.PCScraper(driver[8], dataset['PC'], 'https://phongvu.vn/c/pc/')
    PVU.Scraper(driver[8], dataset['Mouse'], 'https://phongvu.vn/c/chuot/')
    PVU.Scraper(driver[8], dataset['Keyboard'], 'https://phongvu.vn/c/ban-phim-van-phong/')

def pushDataToMySQL(dataset, table):
    db = mysql.connector.connect(
        host="aws.connect.psdb.cloud",
        user=config.USER,
        password=config.PASSWORD,
        database="products"
    )

    sql_insert = ""
    if table == 'Laptop':
        sql_insert = """INSERT INTO Laptop VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    elif table == 'PC':
        sql_insert = """INSERT INTO PC VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    elif table == 'Screen':
        sql_insert = """INSERT INTO Screen VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    else:
        sql_insert = """INSERT INTO {} VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""".format(table)

    mycursor = db.cursor(buffered=True)
    mycursor.execute("DELETE FROM {}".format(table)) 
    count = 0
    for data in dataset[table]:        
        count += 1
        try:     
            mycursor.execute(sql_insert, (count,) + data)
            db.commit()
            print("Pushed row {} to database".format(count))
        except:
            print("Dropped row {} to database".format(count))
            continue
    # mycursor.execute("DELETE FROM {}".format(old_table))  





#--------------MAIN PROGRAM-----------------------------------

# create threads
t = ['' for _ in range(NUMBER_OF_THREADS)]
t[0] = threading.Thread(target = scrapeTGD0)
t[1] = threading.Thread(target = scrapeTGD1)
t[2] = threading.Thread(target = scrapeTGD2)
t[3] = threading.Thread(target = scrapeFPT0)
t[4] = threading.Thread(target = scrapeFPT1)
t[5] = threading.Thread(target = scrapeTPR0)
t[6] = threading.Thread(target = scrapePVU0)
t[7] = threading.Thread(target = scrapePVU1)
t[8] = threading.Thread(target = scrapePVU2)

# for scraping data
def SCRAPE():
    # run threads
    for i in range(NUMBER_OF_THREADS):
        t[i].start()
    # wait until all threads finish
    for i in range(NUMBER_OF_THREADS):
        t[i].join()
    # quit the drivers
    for i in range(NUMBER_OF_THREADS):
        driver[i].quit()

# for inserting data to database
def PUSH():
    pushDataToMySQL(dataset, 'Laptop')
    pushDataToMySQL(dataset, 'PC')
    pushDataToMySQL(dataset, 'Screen')
    pushDataToMySQL(dataset, 'Mouse')
    pushDataToMySQL(dataset, 'Keyboard')

# update all the database
def UPDATE():
    start = time.time()
    SCRAPE()
    PUSH()
    end = time.time()   
    print("TOTAL TIME: ", end - start)





#----------------SCHEDULING--------------------
schedule.every(1).day.do(UPDATE)
UPDATE()
while True:
    schedule.run_pending()
    time.sleep(1)