from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
from random import randint
import time
from scrape import data_standardize

def LaptopScraper(driver, products, url):
    start = time.time()
    prev_len = len(products)
    # get the web page
    driver.get(url)
    type = 'Laptop'
    # id = 1

    # click the button at most 100 times to load more products
    for n in range(100):
        try:
            button = driver.find_element(By.CSS_SELECTOR, "#categoryPage > div.container-productbox > div.view-more > a")
            button.click()
            s = randint(1, 2)
            time.sleep(0.3)
            print('clicked ' + str(n))
        except:
            print('failed ' + str(n))
            continue

    # page_source is a variable created by Selenium - it holds all the HTML
    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")
    tiles = soup.select("div.container-productbox > ul > li")

    SCROLL_PAUSE_TIME = 1.5
    i = 0
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        i += 1
        print(i)
        if i == 5:
            break
    driver.implicitly_wait(2)

    cnt = 0    
    print('TGD laptop ' + str(len(tiles)) + ' tiles')
    for tile in tiles:
        name = tile.find('h3').get_text().strip()
        try:
            price = tile.find('strong', class_="price").get_text()
        except:
            continue
        info_link = 'https://www.thegioididong.com' + tile.find('a').get("href")
        
        img_link = tile.find('img').get("data-src")
        if img_link is None:
            img_link = tile.find('img').get("src")

        gpu = ''
        for _ in range(15):
            driver.get(info_link)
            src = driver.page_source
            soup = BeautifulSoup(src, "html.parser")

            try:
                screen = soup.select_one('div.parameter ul li:nth-child(4) div').get_text()
                cpu = soup.select_one('div.parameter ul li:nth-child(1) div').get_text()
                ram = soup.select_one('div.parameter ul li:nth-child(2) div').get_text()
                disk = soup.select_one('div.parameter ul li:nth-child(3) div').get_text()
                gpu = soup.select_one('div.parameter ul li:nth-child(5) div').get_text()
            except:
                driver.implicitly_wait(2) 
            if gpu != '': break
            
        screen = data_standardize.extract_screen(screen)
        cpu = data_standardize.extract_cpu(cpu)
        ram = data_standardize.extract_ram(ram)
        disk = data_standardize.extract_disk(disk)
        
        product = {
                    # "id": id,
                   "name": name, 
                   "price": data_standardize.price_to_int(price),
                   "info_link": info_link, 
                   "img_link": img_link, 
                   "brand": data_standardize.extract_brand(name),
                   "screen": screen,
                   "cpu": cpu,
                   "ram": ram,
                   "disk_type": disk[0],
                   "disk_storage": disk[1],
                   "gpu": gpu,
                   "shop": "tgd",
                   "type": type,
        }

        print()
        print(product)
        cnt += 1
        print(cnt)


        product_t = tuple(product.values())
        if (product_t[1] == 0) or (product_t[3] == None) or (product_t[10] == '') or (product_t in products):
            continue
        products.add(product_t)
        # id += 1

    end = time.time()
    print("{} {}. {}".format("tgd", len(products) - prev_len, type, end-start))

def PCScraper(driver, products, url):
    start = time.time()
    prev_len = len(products)
    # get the web page
    driver.get(url)
    type = 'PC'
    # id = 1

    # click the button at most 20 times to load more products
    for n in range(40):
        try:
            button = driver.find_element(By.CSS_SELECTOR, "#categoryPage > div.container-productbox > div.view-more > a")
            button.click()
            s = randint(1, 2)
            time.sleep(0.5)
        except:
            continue

    # page_source is a variable created by Selenium - it holds all the HTML
    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")
    tiles = soup.select("div.container-productbox > ul > li")
    
    SCROLL_PAUSE_TIME = 1.5
    i = 0
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        i += 1
        print(i)
        if i == 5:
            break
    driver.implicitly_wait(0.2)

    print(str(len(tiles)) + ' tiles')
    for tile in tiles:
        name = tile.find('h3').get_text().strip()
        try:
            price = tile.find('strong', class_="price").get_text()
        except:
            continue
        info_link = 'https://www.thegioididong.com' + tile.find('a').get("href")
        
        img_link = tile.find('img').get("data-src")
        if img_link is None:
            img_link = tile.find('img').get("src")

        for _ in range(20):
            driver.get(info_link)
            src = driver.page_source
            soup = BeautifulSoup(src, "html.parser")

            try:
                button = driver.find_element(By.CLASS_NAME, "btn-detail.btn-short-spec.not-have-instruction")
                button.click()
            except:
                try:
                    button = driver.find_element(By.CSS_SELECTOR, "body > section.detail > div.box_main > div.box_right > div.parameter > span.btn-detail.btn-short-spec")
                    button.click()
                except:
                    print("click failed")
                    

            time.sleep(0.5)
            driver.implicitly_wait(2) 
            src = driver.page_source
            soup = BeautifulSoup(src, "html.parser")
            time.sleep(0.5)
            driver.implicitly_wait(2) 

            cpu, ram, disk = '', '', ''
            try:
                cpu = soup.select_one('#tab-content-specification-gallery-0 > div > div > div:nth-child(1) > ul > li:nth-child(1) > div.ctRight > a').get_text()
            except:
                driver.implicitly_wait(0.2) 
            try:
                ram = soup.select_one('#tab-content-specification-gallery-0 > div > div > div:nth-child(2) > ul > li:nth-child(1) > div.ctRight > a').get_text()
            except:
                driver.implicitly_wait(0.2) 
            try:            
                disk = soup.select_one('#tab-content-specification-gallery-0 > div > div > div:nth-child(2) > ul > li:nth-child(6) > div.ctRight > a').get_text()
            except:
                driver.implicitly_wait(0.2) 
            
            if cpu == None or cpu == '':
                try:
                    cpu = soup.select_one('#tab-content-specification-gallery-0 > div > div > div:nth-child(1) > ul > li:nth-child(1) > div.ctRight > span').get_text()
                except:
                    print("fail")
            if ram == None or ram == '':
                try:
                    ram = soup.select_one('#tab-content-specification-gallery-0 > div > div > div:nth-child(2) > ul > li:nth-child(1) > div.ctRight > span').get_text()
                except:
                    print("fail")
            if disk == None or disk == '':
                try:
                    disk = soup.select_one('#tab-content-specification-gallery-0 > div > div > div:nth-child(2) > ul > li:nth-child(6) > div.ctRight > span').get_text()
                except:
                    print("fail")
            
            
            if cpu == None or cpu == '':
                try:
                    cpu = soup.select_one('body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(1) > div').get_text()
                except:
                    print("fail2")
            if ram == None or ram == '':
                try:
                    ram = soup.select_one('body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(2) > div').get_text()
                except:
                    print("fail2")
            if disk == None or disk == '':
                try:
                    disk = soup.select_one('body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(3) > div').get_text()
                except:
                    print("fail2")

            if cpu != '': break


        cpu = data_standardize.extract_cpu(cpu)
        ram = data_standardize.extract_ram(ram)
        disk = data_standardize.extract_disk(disk)
        
        product = {
                    # "id": id,
                   "name": name, 
                   "price": data_standardize.price_to_int(price),
                   "info_link": info_link, 
                   "img_link": img_link, 
                   "brand": data_standardize.extract_brand(name),
                   "cpu": cpu,
                   "ram": ram,
                   "disk_type": disk[0],
                   "disk_storage": disk[1],
                   "shop": "tgd",
                   "type": type,
        }

        print()
        print(product)

        product_t = tuple(product.values())
        if (product_t[1] == 0) or (product_t[3] == None) or (product_t[5] == '') or (product_t in products):
            continue
        products.add(product_t)
        # id += 1

    end = time.time()
    print("{} {}. {}".format("tgd", len(products) - prev_len, type, end-start))

def ScreenScraper(driver, products, url):
    start = time.time()
    prev_len = len(products)
    # get the web page
    driver.get(url)
    type = 'Screen'
    # id = 1

    # click the button at most 20 times to load more products
    for n in range(40):
        try:
            button = driver.find_element(By.CSS_SELECTOR, "#categoryPage > div.container-productbox > div.view-more > a")
            button.click()
            s = randint(1, 2)
            time.sleep(0.5)
        except:
            continue

    # page_source is a variable created by Selenium - it holds all the HTML
    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")
    tiles = soup.select("div.container-productbox > ul > li")

    SCROLL_PAUSE_TIME = 1.5
    i = 0
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        i += 1
        print(i)
        if i == 5:
            break
    driver.implicitly_wait(2)

    for tile in tiles:
        name = tile.find('h3').get_text().strip()
        try:
            price = tile.find('strong', class_="price").get_text()
        except:
            continue
        info_link = 'https://www.thegioididong.com' + tile.find('a').get("href")
        
        img_link = tile.find('img').get("data-src")
        if img_link is None:
            img_link = tile.find('img').get("src")

        screen = ''
        for _ in range(15):
            driver.get(info_link)
            src = driver.page_source
            soup = BeautifulSoup(src, "html.parser")

            try:
                screen = soup.select_one('div.parameter ul li:nth-child(2) div').get_text()
            except:
                driver.implicitly_wait(2) 
            if screen != '': break

        tmp = screen
        screen = data_standardize.extract_screen(tmp)
        refresh_rate = data_standardize.extract_refresh_rate(tmp)

        product = {
                    # "id": id,
                   "name": name, 
                   "price": data_standardize.price_to_int(price),
                   "info_link": info_link, 
                   "img_link": img_link, 
                   "brand": data_standardize.extract_brand(name),
                   "screen": screen,
                   "refresh_rate": refresh_rate,
                   "shop": "tgd",
                   "type": type,
        }

        print()
        print(product)

        product_t = tuple(product.values())
        if (product_t[1] == 0) or (product_t[3] == None) or (product_t[5] == '') or (product_t in products):
            continue
        products.add(product_t)
        # id += 1

    end = time.time()
    print("{} {}. {}".format("tgd", len(products) - prev_len, type, end-start)) 

def Scraper(driver, products, url):
    if ('chuot-may-tinh' in url):
        type = 'Mouse'
    else:
        type = 'Keyboard'
    # id = 1

    start = time.time()
    prev_len = len(products)
    # get the web page
    driver.get(url)

    # click the button at most 20 times to load more products
    for n in range(40):
        try:
            button = driver.find_element(By.CSS_SELECTOR, "#categoryPage > div.container-productbox > div.view-more > a")
            button.click()
            s = randint(1, 2)
            time.sleep(s * 0.05)
        except:
            continue

    SCROLL_PAUSE_TIME = 1.5
    i = 0
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        i += 1
        if i == 5:
            break
    driver.implicitly_wait(2)

    # page_source is a variable created by Selenium - it holds all the HTML
    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")
    tiles = soup.select("#categoryPage > div.container-productbox > ul > *")

    for tile in tiles:
        name = tile.find('h3').get_text().strip()
        try:
            price = tile.find('strong', class_="price").get_text()
        except:
            continue
        info_link = 'https://www.thegioididong.com' + tile.find('a').get("href")
        img_link = tile.find('img').get("data-src")
        product = {
                    # "id": id,
                   "name": name, 
                   "price": data_standardize.price_to_int(price),
                   "info_link": info_link, 
                   "img_link": img_link, 
                   "brand": data_standardize.extract_brand(name),
                   "shop": "tgd",
                   "type": type
        }

        print()
        print(product)

        product_t = tuple(product.values())
        if (product_t[1] == 0) or (product_t[3] == None) or (product_t in products):
            continue
        products.add(product_t)
        # id += 1

    end = time.time()
    print("{} {}. {}".format("tgd", len(products) - prev_len, type, end-start))