from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
from random import randint
import time
from scrape import data_standardize

def LaptopScraper(driver, dataset, url):
    start = time.time()
    prev_len = len(dataset)

    # get the web page
    driver.get(url)
    type = 'Laptop'
    # id = 1

    # click the button at most 20 times to load more products
    for n in range(20):
        try:
            button = driver.find_element(By.CSS_SELECTOR, "div.fplistbox > div > div:nth-child(3)")
            button.click()
            s = randint(1, 2)
            time.sleep(0.7)
        except:
            break

    # page_source is a variable created by Selenium - it holds all the HTML
    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")
    tiles = soup.select("div.fplistbox > div > div:nth-child(2) > .cdt-product, .cate-product")

    #scroll page for lazy-loaded images
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
    driver.implicitly_wait(15)          # allow catchup for any remaining images that are still loading in

    for tile in tiles:     
        href = tile.find('a').get("href")
        info_link = 'https://fptshop.com.vn' + href

        name, disk = '', ''
        for _ in range(10):
            driver.get(info_link)
            src = driver.page_source
            soup = BeautifulSoup(src, "html.parser")
            try:
                name = soup.select_one('h1.st-name').get_text()
                price = soup.select_one('div.st-price-main').get_text()
                brand = soup.select_one('li.breadcrumb-item.active a').get_text().upper()
                img_link = soup.select_one('div.swiper-slide.swiper-slide-active img').get('src')
                screen = soup.select_one('div.st-param ul li:nth-child(1) p').get_text()
                cpu = soup.select_one('div.st-param ul li:nth-child(2) p').get_text()
                ram = soup.select_one('div.st-param ul li:nth-child(3) p').get_text()
                disk = soup.select_one('div.st-param ul li:nth-child(4) p').get_text()
                gpu = soup.select_one('div.st-param ul li:nth-child(5) p').get_text()
            except:
                time.sleep(0.5)
            if name != '' and disk != '': break        
        
        print()
        print(info_link)
        print(cpu)

        screen = data_standardize.extract_screen(str(screen))
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
                   "shop": "fpt",
                   "type": type,
        }

        # print()
        print(product)

        product_t = tuple(product.values())
        if product_t[0] == '' or product_t[1] == 0 or (product_t[3] == None) or (product_t in dataset):
            continue
        dataset.add(product_t)
        # id += 1

    end = time.time()
    print("{} {}. {}".format("fpt", len(dataset) - prev_len, type, end-start))

def PCScraper(driver, dataset, url):
    start = time.time()
    prev_len = len(dataset)

    # get the web page
    driver.get(url)
    type = 'PC'
    # id = 1

    # click the button at most 20 times to load more products
    for n in range(20):
        try:
            button = driver.find_element(By.CSS_SELECTOR, "div.fplistbox > div > div:nth-child(3)")
            button.click()
            s = randint(1, 2)
            time.sleep(0.7)
        except:
            continue

    # page_source is a variable created by Selenium - it holds all the HTML
    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")
    tiles = soup.select("div.fplistbox > div > div:nth-child(2) > .cdt-product, .cate-product")

    #scroll page for lazy-loaded images
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
    driver.implicitly_wait(10)          # allow catchup for any remaining images that are still loading in

    for tile in tiles:     
        href = tile.find('a').get("href")
        info_link = 'https://fptshop.com.vn' + href

        name, img_link, cpu = '', '', ''
        for _ in range(10):
            driver.get(info_link)
            src = driver.page_source
            soup = BeautifulSoup(src, "html.parser")
            try:
                name = soup.select_one('h1.st-name').get_text()
                price = soup.select_one('div.st-price-main').get_text()
                brand = soup.select_one('li.breadcrumb-item.active a').get_text()
                img_link = soup.select_one('div.swiper-slide.swiper-slide-active img').get('src')
                cpu = soup.select_one('div.st-param ul li:nth-child(1) p').get_text()
                ram = soup.select_one('div.st-param ul li:nth-child(2) p').get_text()
                disk = soup.select_one('div.st-param ul li:nth-child(3) p').get_text()
                info = cpu + ' ' + ram + ' ' + disk
            except:
                time.sleep(0.5)
            if name != '' and img_link != '' and cpu != '': break    

        print()
        print(info_link)
        print(info)

        tmp = name
        tmp = tmp.replace('/', ' ')
        tmp = tmp.replace('-', ' ')
        # if (data_standardize.extract_screen(cpu) != None):
        cpu = data_standardize.extract_cpu(info) 
        ram = data_standardize.extract_ram(info)
        disk = data_standardize.extract_disk(info)   
        if disk == None:
            disk = data_standardize.extract_disk(tmp)
        
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
                   "shop": "fpt",
                   "type": type,
        }

        # print()
        print(product)

        product_t = tuple(product.values())
        if product_t[0] == '' or product_t[1] == 0 or (product_t[3] == None) or (product_t in dataset):
            continue
        dataset.add(product_t)
        # id += 1

    end = time.time()
    print("{} {}. {}".format("fpt", len(dataset) - prev_len, type, end-start))

def ScreenScraper(driver, dataset, url):

    start = time.time()
    prev_len = len(dataset)

    # get the web page
    driver.get(url)
    type = 'Screen'
    # id = 1

    # click the button at most 20 times to load more products
    for n in range(20):
        try:
            button = driver.find_element(By.CSS_SELECTOR, "div.fplistbox > div > div:nth-child(3)")
            button.click()
            s = randint(1, 2)
            time.sleep(0.7)
        except:
            continue

    # page_source is a variable created by Selenium - it holds all the HTML
    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")
    tiles = soup.select("div.fplistbox > div > div:nth-child(2) > .cdt-product, .cate-product")

    #scroll page for lazy-loaded images
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
    driver.implicitly_wait(10)          # allow catchup for any remaining images that are still loading in

    for tile in tiles:     
        href = tile.find('a').get("href")
        info_link = 'https://fptshop.com.vn' + href

        name, img_link, screen = '', '', ''
        for _ in range(10):
            driver.get(info_link)
            src = driver.page_source
            soup = BeautifulSoup(src, "html.parser")
            try:
                name = soup.select_one('h1.st-name').get_text()
                price = soup.select_one('div.st-price-main').get_text()
                brand = soup.select_one('li.breadcrumb-item.active a').get_text()
                img_link = soup.select_one('div.swiper-slide.swiper-slide-active img').get('src')
                screen = soup.select_one('div.st-param ul li:nth-child(1) p').get_text()
                refresh_rate = soup.select_one('tbody > tr:nth-child(2) > td:nth-child(2)').get_text()
            except:
                time.sleep(0.5)
            if name != '' and img_link != '' and screen != '': break        
            
        screen = data_standardize.extract_screen(screen)
        refresh_rate = data_standardize.extract_refresh_rate(refresh_rate)

        product = {
                    # "id": id,
                   "name": name, 
                   "price": data_standardize.price_to_int(price),
                   "info_link": info_link, 
                   "img_link": img_link, 
                   "brand": data_standardize.extract_brand(name),
                   "screen": screen,
                   "refresh_rate": refresh_rate,
                   "shop": "fpt",
                   "type": type,
        }

        print()
        print(product)

        product_t = tuple(product.values())
        if product_t[0] == '' or product_t[1] == 0 or (product_t[3] == None) or (product_t in dataset):
            continue
        dataset.add(product_t)
        # id += 1

    end = time.time()
    print("{} {}. {}".format("fpt", len(dataset) - prev_len, type, end-start))

def Scraper(driver, dataset, url):
    if ('chuot' in url):
        type = 'Mouse'
    else:
        type = 'Keyboard'
    # id = 1

    start = time.time()
    prev_len = len(dataset)
    # get the web page
    driver.get(url)

    # click the button at most 20 times to load more products
    for n in range(20):
        try:
            button = driver.find_element(By.CSS_SELECTOR, "body main section.section-common div div.section-normal div a.btn.btn-secondary.btn-viewmore")
            button.click()
            s = randint(1, 2)
            time.sleep(0.5)
        except:
            continue

    # scroll page for lazy-loaded images
    SCROLL_PAUSE_TIME = 1
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
    driver.implicitly_wait(15)          # allow catchup for any remaining images that are still loading in

    # page_source is a variable created by Selenium - it holds all the HTML
    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")
    tiles = soup.select("div.normal-body > .product-item")
    #print("--------------------------------------------------------------------------\t", len(tiles))

    for tile in tiles:
        name = tile.find('h3').get_text().strip()
        info_link = 'https://fptshop.com.vn' + tile.find('a').get("href")

        img_link = ''
        for _ in range(10):
            driver.get(info_link)
            src = driver.page_source
            soup = BeautifulSoup(src, "html.parser")
            try:
                price = soup.select_one('div.st-price-main').get_text()
                brand = soup.select_one('div.l-pd-top span').get_text()
                img_link = soup.select_one('div.swiper-slide.swiper-slide-active img').get('src')
            except:
                print(_ * 10)
                time.sleep(0.2)
            if price and img_link: break
        
        product = {
                    # "id": id,
                   "name": name, 
                   "price": data_standardize.price_to_int(price),
                   "info_link": info_link, 
                   "img_link": img_link, 
                   "brand": data_standardize.extract_brand(name),
                   "shop": "fpt",
                   "type": type
        }

        print()
        print(product)

        product_t = tuple(product.values())
        if not product_t[0] or product_t[1] == 0 or (product_t[3] == None) or (product_t in dataset):
            continue
        dataset.add(product_t)
        # id += 1

    end = time.time()
    print("{} {}. {}".format("fpt", len(dataset) - prev_len, type, end-start))