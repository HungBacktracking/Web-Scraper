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
    i = 0

    # click the button at most 20 times to load more products
    for n in range(100):
        try:
            button = driver.find_element(By.CSS_SELECTOR, "div.mt-8.container > div.mt-6.flex.justify-center > button")
            button.click()
            #print("---------------------------------------------------OK")
            s = randint(1, 2)
            time.sleep(0.5)
            print('click ' + str(n))
        except:
            print('failed ' + str(n))
            continue

    # page_source is a variable created by Selenium - it holds all the HTML
    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")
    tiles = soup.select("#__layout > div > main > div.mt-8.container > div.mt-4 > section > div > a")
    print(len(tiles))#__layout > div > main > div.mt-8.container > div.mt-4 > section > div > a:nth-child(16)
    
    
    # scroll page for lazy-loaded images
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
    driver.implicitly_wait(15)          # allow catchup for any remaining images that are still loading in

    cnt = 0
    print('TPR laptop ' + str(len(tiles)) + ' tiles')
    for tile in tiles:
        name = tile.find('div', class_='t-product-item__title').get_text().strip()
        price = tile.find('span', class_='t-product-item__price').get_text()
        info_link = 'https://www.thinkpro.vn' + tile.get("href")
        img_link = tile.find('img').get("data-src")

        gpu = ''
        for _ in range(25):
            driver.get(info_link)
            src = driver.page_source
            soup = BeautifulSoup(src, "html.parser")
            try:
                screen = soup.select_one('div.section-attribute-content.mt-5.grid.grid-cols-2.gap-4 > div:nth-child(5) > div:nth-child(2) > span:nth-child(2)').get_text()
            except:
                screen = None
            try:
                cpu = soup.select_one('div.section-attribute-content.mt-5.grid.grid-cols-2.gap-4 > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)').get_text()
            except:
                cpu = None
            try:
                ram = soup.select_one('div.section-attribute-content.mt-5.grid.grid-cols-2.gap-4 > div:nth-child(3) > div:nth-child(2) > span:nth-child(2)').get_text()
            except:
                ram = None
            try:
                disk = soup.select_one('div.section-attribute-content.mt-5.grid.grid-cols-2.gap-4 > div:nth-child(4) > div:nth-child(2) > span:nth-child(1)').get_text() + soup.select_one('div.section-attribute-content.mt-5.grid.grid-cols-2.gap-4 > div:nth-child(4) > div:nth-child(2) > span:nth-child(2)').get_text()
                disk = disk.replace(":", " ")
            except:
                disk = None
            try:
                gpu = soup.select_one('div.section-attribute-content.mt-5.grid.grid-cols-2.gap-4 > div:nth-child(2) > div:nth-child(2) > span:nth-child(2)').get_text()
            except:
                try:
                    gpu = soup.select_one('div.section-attribute-content.mt-5.grid.grid-cols-2.gap-4 > div:nth-child(2) > div:nth-child(2) > span:nth-child(1)').get_text()
                except:
                    gpu = None
            if gpu != '': 
                break
        

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
                   "shop": "tpr",
                   "type": type,
        }
        
        print()
        print(product)
        cnt+=1
        print(cnt)

        product_t = tuple(product.values())
        if (product_t[1] == 0) or (product_t[3] == None) or (product_t[10] == '') or (product_t in dataset):
            continue
        dataset.add(product_t)

    
    end = time.time()
    print("{} {}. {}".format("tpr", len(dataset) - prev_len, type, end-start))

def Scraper(driver, dataset, url):
    if (url.endswith('chuot')):
        type = 'Mouse'
    else:
        type = 'Keyboard'
    # id = 1

    start = time.time()
    prev_len = len(dataset)

    # get the web page
    driver.get(url)

    # click the button at most 20 times to load more products
    for n in range(50):
        try:
            button = driver.find_element(By.CSS_SELECTOR, "div.mt-8.container > div.mt-6.flex.justify-center > button")
            button.click()
            #print("---------------------------------------------------OK")
            s = randint(1, 2)
            time.sleep(s * 0.1)
        except:
            continue
    
    # scroll page for lazy-loaded images
    SCROLL_PAUSE_TIME = 0.5
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
    ##driver.implicitly_wait(10)          # allow catchup for any remaining images that are still loading in

    # page_source is a variable created by Selenium - it holds all the HTML
    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")
    tiles = soup.select("#__layout > div > main > div.mt-8.container > div.mt-4 > section > div > a")
    print(len(tiles))
    cnt=0
    for tile in tiles:
        name = tile.find('div', class_='t-product-item__title').get_text().strip()
        price = tile.find('span', class_='t-product-item__price').get_text()
        info_link = 'https://www.thinkpro.vn' + tile.get("href")
        img_link = tile.find('img').get("data-src")
        product = {
                    # "id": id,
                   "name": name, 
                   "price": data_standardize.price_to_int(price),
                   "info_link": info_link, 
                   "img_link": img_link, 
                   "brand": data_standardize.extract_brand(name),
                   "shop": "tpr",
                   "type": type
        }
        
        print()
        print(product)

        product_t = tuple(product.values())
        if (product_t[1] == 0) or (product_t[3] == None) or (product_t in dataset):
            continue
        dataset.add(product_t)
        cnt += 1
        print(cnt)

    
    end = time.time()
    print("{} {}. {}".format("tpr", len(dataset) - prev_len, type, end-start))