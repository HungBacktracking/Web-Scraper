from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
from random import randint
import time
import regex as re
from scrape import data_standardize

def LaptopScraper(driver, dataset, url):
    start = time.time()
    prev_len = len(dataset)
    type = 'Laptop'
    # id = 1
    
    # get number of pages
    driver.get(url)
    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    N_page = soup.select_one("#__next > div > div > div > div > div:nth-child(4) > div:nth-child(2) > div > div.teko-col.teko-col-10.css-gr7r8o > div.teko-row.css-16rlp3f > div > div > a:nth-last-child(2) > div").get_text()
    N_page = int(N_page)
    print(N_page)

    # browse N_page pages
    for n in range(1, N_page + 1):    

        # page_source is a variable created by Selenium - it holds all the HTML
        page_url = url + "?page=" + str(n)
        driver.get(page_url)
        page = driver.page_source
        soup = BeautifulSoup(page, "html.parser")
        tiles = soup.find_all('div', class_="css-13w7uog")  
        

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

        for tile in tiles:
            
            info_link = 'https://phongvu.vn' + tile.find('a').get("href")

            img_link, info = '', ''
            for _ in range(15):
                driver.get(info_link)
                page = driver.page_source
                soup = BeautifulSoup(page, "html.parser")

                try:
                    img_link = soup.select_one('div.productDetailPreview img').get("src")
                    product_name = soup.select_one('div.css-6b3ezu h1').get_text()
                    if 'Liên hệ đặt hàng' in product_name:
                        product_name = product_name[16:]
                    brand = soup.select_one('div.css-6b3ezu a span').get_text()
                    price = soup.select_one('div.css-1q5zfcu div').get_text()

                    info = soup.select_one('div.css-17aam1').get_text()
                except:
                    driver.implicitly_wait(1)
                if  img_link != '' and info != '': break
            try: 
                info = info.replace('&nbsp;', ' ') # replace '&nbsp;' with ' '
                info_in_bracket = re.search(r'\(.*\)', info)
                if info_in_bracket:
                    info = info.replace(info_in_bracket.group(), "")
                list_info = info.split("- ")
                cpu = list_info[1]
                ram = list_info[3]
                gpu = list_info[4]
                screen = list_info[2]
                disk = list_info[5]
            except:
                continue

            print()
            print(info_link)

            screen = data_standardize.extract_screen(screen)
            cpu = data_standardize.extract_cpu(cpu)
            ram = data_standardize.extract_ram(ram)
            disk = data_standardize.extract_disk(disk)
            
            product = {
                    # "id": id,
                    "name": product_name, 
                    "price": data_standardize.price_to_int(price),
                    "info_link": info_link, 
                    "img_link": img_link, 
                    "brand": data_standardize.extract_brand(product_name),
                    "screen": screen,
                    "cpu": cpu,
                    "ram": ram,
                    "disk_type": disk[0],
                    "disk_storage": disk[1],
                    "gpu": gpu,
                    "shop": "pvu",
                    "type": type,
            }
        
            print()
            print(product)

            product_t = tuple(product.values())
            if (product_t[1] == 0) or (product_t[3] == None) or (product_t[9] == None) or (product_t in dataset):
                if (product_t in dataset):
                    continue
            dataset.add(product_t)
            # id += 1


        # for i in range(10):
        #     try:
        #         driver.get(url)
        #         button = driver.find_element(By.CSS_SELECTOR, "#__next > div > div > div > div > div:nth-child(4) > div:nth-child(2) > div > div.teko-col.teko-col-10.css-gr7r8o > div.teko-row.css-16rlp3f > div > div > div:last-child")
        #         button.click()
        #         s = randint(1, 2)
        #         #print("--------------------------------------------------------------------------       ", n)
        #         time.sleep(s * 0.005)
        #         break
        #     except:
        #         continue
    end = time.time()
    print("{} {}. {}".format("pvu", len(dataset) - prev_len, type, end-start))

def PCScraper(driver, dataset, url):
    i = 0
    start = time.time()
    prev_len = len(dataset)
    type = 'PC'
    # id = 1

    # get number of pages
    driver.get(url)
    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    N_page = soup.select_one("#__next > div > div > div > div > div:nth-child(4) > div:nth-child(2) > div > div.teko-col.teko-col-10.css-gr7r8o > div.teko-row.css-16rlp3f > div > div > a:nth-last-child(2) > div").get_text()
    N_page = int(N_page)
    print(N_page)

    # browse N_page pages
    for n in range(1, N_page + 1):       

        # page_source is a variable created by Selenium - it holds all the HTML
        page_url = url + "?page=" + str(n)
        driver.get(page_url)
        page = driver.page_source
        soup = BeautifulSoup(page, "html.parser")
        tiles = soup.find_all('div', class_="css-13w7uog")   

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

        for tile in tiles:
            
            info_link = 'https://phongvu.vn' + tile.find('a').get("href")

            img_link = ''
            for _ in range(10):
                driver.get(info_link)
                page = driver.page_source
                soup = BeautifulSoup(page, "html.parser")

                try:
                    img_link = soup.select_one('div.productDetailPreview img').get("src")
                    product_name = soup.select_one('div.css-6b3ezu h1').get_text()
                    if 'Liên hệ đặt hàng' in product_name:
                        product_name = product_name[16:]
                    brand = soup.select_one('div.css-6b3ezu a span').get_text()
                    price = soup.select_one('div.css-1q5zfcu div').get_text()
                except:
                    driver.implicitly_wait(15) 
                if img_link != '': break


            print()
            print(info_link)

            tmp = product_name
            tmp = tmp.replace('/', ' ')
            print(tmp)
            cpu = data_standardize.extract_cpu(tmp)
            disk = data_standardize.extract_disk(tmp)
            tmp = tmp.replace(str(disk), "")
            ram = data_standardize.extract_ram(tmp)
            
            product = {
                    # "id": id,
                    "name": product_name, 
                    "price": data_standardize.price_to_int(price),
                    "info_link": info_link, 
                    "img_link": img_link, 
                    "brand": data_standardize.extract_brand(product_name),
                    "cpu": cpu,
                    "ram": ram,
                    "disk_type": disk[0],
                    "disk_storage": disk[1],
                    "shop": "pvu",
                    "type": type,
            }
        
            print()
            print(product)

            product_t = tuple(product.values())
            if (product_t[1] == 0) or (product_t[3] == None) or (product_t in dataset):
                if (product_t in dataset):
                    continue
            dataset.add(product_t)
            # id += 1
            i += 1

        # try:
        #     driver.get(url)
        #     button = driver.find_element(By.CSS_SELECTOR, "#__next > div > div > div > div > div:nth-child(4) > div:nth-child(2) > div > div.teko-col.teko-col-10.css-gr7r8o > div.teko-row.css-16rlp3f > div > div > div:last-child")
        #     button.click()
        #     s = randint(1, 2)
        #     #print("--------------------------------------------------------------------------       ", n)
        #     time.sleep(s * 0.005)
        # except:
        #     break
    end = time.time()
    print("{} {}. {}".format("pvu", len(dataset) - prev_len, type, end-start))

def ScreenScraper(driver, dataset, url):
    i = 0
    start = time.time()
    prev_len = len(dataset)
    # get the web page
    driver.get(url)
    type = 'Screen'
    # id = 1

    # get number of pages
    driver.get(url)
    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    N_page = soup.select_one("#__next > div > div > div > div > div:nth-child(4) > div:nth-child(2) > div > div.teko-col.teko-col-10.css-gr7r8o > div.teko-row.css-16rlp3f > div > div > a:nth-last-child(2) > div").get_text()
    N_page = int(N_page)
    print(N_page)

    # browse N_page pages
    for n in range(1, N_page + 1):    

        # page_source is a variable created by Selenium - it holds all the HTML
        page_url = url + "?page=" + str(n)
        driver.get(page_url)
        page = driver.page_source
        soup = BeautifulSoup(page, "html.parser")
        tiles = soup.find_all('div', class_="css-13w7uog")  

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

        for tile in tiles:
            
            info_link = 'https://phongvu.vn' + tile.find('a').get("href")

            img_link, info = '', ''
            for _ in range(10):
                driver.get(info_link)
                page = driver.page_source
                soup = BeautifulSoup(page, "html.parser")

                try:
                    img_link = soup.select_one('div.productDetailPreview img').get("src")
                    product_name = soup.select_one('div.css-6b3ezu h1').get_text()
                    if 'Liên hệ đặt hàng' in product_name:
                        product_name = product_name[16:]
                    brand = soup.select_one('div.css-6b3ezu a span').get_text()
                    price = soup.select_one('div.css-1q5zfcu div').get_text()

                    info = soup.select_one('div.css-17aam1').get_text()
                except:
                    driver.implicitly_wait(15) 
                if img_link != '' and info != '': break

            info = info.replace("&nbsp;", " ") # replace '&nbsp;' with ' '
            
            tmp = info
            screen = data_standardize.extract_screen(tmp)
            refresh_rate = data_standardize.extract_refresh_rate(tmp)

            product = {
                    # "id": id,
                    "name": product_name, 
                    "price": data_standardize.price_to_int(price),
                    "info_link": info_link, 
                    "img_link": img_link, 
                    "brand": data_standardize.extract_brand(product_name),
                    "screen": screen,
                    "refresh_rate": refresh_rate,
                    "shop": "pvu",
                    "type": type,
            }
            
            print()
            print(product)

            product_t = tuple(product.values())
            if (product_t[1] == 0) or (product_t[3] == None) or (product_t in dataset):
                if (product_t in dataset):
                    continue
            dataset.add(product_t)
            # id += 1

        # try:
        #     driver.get(url)
        #     button = driver.find_element(By.CSS_SELECTOR, "#__next > div > div > div > div > div:nth-child(4) > div:nth-child(2) > div > div.teko-col.teko-col-10.css-gr7r8o > div.teko-row.css-16rlp3f > div > div > div:last-child")
        #     button.click()
        #     s = randint(1, 2)
        #     #print("--------------------------------------------------------------------------       ", n)
        #     time.sleep(s * 0.005)
        # except:
        #     break
    end = time.time()
    print("{} {}. {}".format("pvu", len(dataset) - prev_len, type, end-start))

def Scraper(driver, dataset, url):
    if ('chuot' in url):
        type = 'Mouse'
    else:
        type = 'Keyboard'
    # id = 1

    start = time.time()
    prev_len = len(dataset)    

    # get number of pages
    driver.get(url)
    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    N_page = soup.select_one("#__next > div > div > div > div > div:nth-child(4) > div:nth-child(2) > div > div.teko-col.teko-col-10.css-gr7r8o > div.teko-row.css-16rlp3f > div > div > a:nth-last-child(2) > div").get_text()
    N_page = int(N_page)
    print(N_page)

    # browse N_page pages
    for n in range(1, N_page + 1):     

        # page_source is a variable created by Selenium - it holds all the HTML
        page_url = url + "?page=" + str(n)
        driver.get(page_url)
        page = driver.page_source
        soup = BeautifulSoup(page, "html.parser")
        tiles = soup.find_all('div', class_="css-13w7uog")    

        for tile in tiles:
            name = tile.find('h3').get_text().strip()
            if 'Liên hệ đặt hàng' in name:
                name = name[16:]
            price = tile.find('div', {'class': 'css-1co26wt'}).find('div', {'type': 'subtitle'}).get_text().strip()
            info_link = 'https://phongvu.vn' + tile.find('a').get("href")
            img_link = tile.find('img').get("src")
            brand = tile.find('div', {'class': 'css-68cx5s'}).find('div').get_text().strip().upper()

            product = {
                #    "id": id,
                   "name": name, 
                   "price": data_standardize.price_to_int(price),
                   "info_link": info_link, 
                   "img_link": img_link, 
                   "brand": data_standardize.extract_brand(name),
                   "shop": "pvu",
                   "type": type
            }
        
            print()
            print(product)

            product_t = tuple(product.values())
            if (product_t[1] == 0) or (product_t[3] == None) or (product_t in dataset):
                continue
            dataset.add(product_t)
            # id += 1

    

        # try:
        #     button = driver.find_element(By.CSS_SELECTOR, "#__next > div > div > div > div > div:nth-child(4) > div:nth-child(2) > div > div.teko-col.teko-col-10.css-gr7r8o > div.teko-row.css-16rlp3f > div > div > div:last-child")
        #     button.click()
        #     s = randint(1, 2)
        #     #print("--------------------------------------------------------------------------       ", n)
        #     time.sleep(s * 0.005)
        # except:
        #     break
    end = time.time()
    print("{} {}. {}".format("pvu", len(dataset) - prev_len, type, end-start))