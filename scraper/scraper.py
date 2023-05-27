from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
from random import randint
import time
import data_standardize_old
    

def scrape_tgd(driver, products, url):
    start = time.time()
    prev_len = len(products)
    # get the web page
    driver.get(url)
    type = data_standardize_old.get_type_slashslash(url)

    # click the button at most 20 times to load more products
    for n in range(40):
        try:
            button = driver.find_element(By.CLASS_NAME, "view-more")
            button.click()
            s = randint(1, 2)
            time.sleep(s * 0.005)
        except:
            continue

    # page_source is a variable created by Selenium - it holds all the HTML
    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")
    tiles = soup.select("#categoryPage > div.container-productbox > ul > *")
    type = data_standardize_old.get_type_slashslash(url)
    type = data_standardize_old.get_true_type(type)

    for tile in tiles:
        name = tile.find('h3').get_text().strip()
        try:
            price = tile.find('strong', class_="price").get_text()
        except:
            continue
        info_link = 'https://www.thegioididong.com' + tile.find('a').get("href")
        img_link = tile.find('img').get("data-src")
        product = {"name": name, 
                   "price": data_standardize_old.get_price(price),
                   "info_link": info_link, 
                   "img_link": img_link, 
                   "shop": "tgd",
                   "brand": data_standardize_old.get_brand(name),
                   "type": type
        }
        product_t = tuple(product.values())
        if (product_t[1] == 0) or (product_t[3] == None) or (product_t in products):
            continue
        products.add(product_t)

    end = time.time()
    print("{} {}. {}".format("tgd", len(products) - prev_len, type, end-start))


def scrape_fpt(driver, products, url):
    start = time.time()
    prev_len = len(products)

    # get the web page
    driver.get(url)  
    type = data_standardize_old.get_type_slashslash(url)
    type = data_standardize_old.get_true_type(type)

    # click the button at most 20 times to load more products
    for n in range(20):
        try:
            button = driver.find_element(By.CSS_SELECTOR, "div.fplistbox > div > div:nth-child(3)")
            button.click()
            s = randint(1, 2)
            time.sleep(s * 0.1)
        except:
            break

    

    

    # page_source is a variable created by Selenium - it holds all the HTML
    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")
    tiles = soup.select("div.fplistbox > div > div:nth-child(2) > .cdt-product, .cate-product ")

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
        print(i)
        if i == 5:
            break
    driver.implicitly_wait(10)          # allow catchup for any remaining images that are still loading in

    for tile in tiles:
        name = tile.find('h3').get_text().strip()
        try:
            price = tile.select("div.progress, div.price, div.price.f-s-p-18")[0].text
        except:
           price = None
        info_link = 'https://fptshop.com.vn' + tile.find('a').get("href")
        
        
        try:
            img_link = tile.select('div:first-child > a:first-child > img:first-child')[0].get('src')
        except:
            img_link = None
        product = {"name": name, 
                   "price": data_standardize_old.get_price(price),
                   "info_link": info_link, 
                   "img_link": img_link, 
                   "shop": "fpt",
                   "brand": data_standardize_old.get_brand(name),
                   "type": type
        }
        product_t = tuple(product.values())
        if product_t[1] == 0 or (product_t[3] == None) or (product_t in products):
            continue
        products.add(product_t)

    end = time.time()
    print("{} {}. {}".format("fpt", len(products) - prev_len, type, end-start))

def scrape_fpt2(driver, products, url):
    start = time.time()
    prev_len = len(products)
    # get the web page
    driver.get(url)
    type = data_standardize_old.get_type_slashslash(url)
    type = data_standardize_old.get_true_type(type)

    # click the button at most 20 times to load more products
    for n in range(20):
        try:
            button = driver.find_element(By.CSS_SELECTOR, "body > main > section.section-common > div > div.section-normal > div > a")
            button.click()
            s = randint(1, 2)
            time.sleep(s * 0.05)
        except:
            break

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
        print(i)
        if i == 5:
            break
    driver.implicitly_wait(10)          # allow catchup for any remaining images that are still loading in

    # page_source is a variable created by Selenium - it holds all the HTML
    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")
    tiles = soup.select("div.normal-body > .product-item")
    #print("--------------------------------------------------------------------------\t", len(tiles))

    for tile in tiles:
        name = tile.find('h3').get_text().strip()
        try:
            price = tile.select("div.product_progress, div.product_main-price")[0].text.strip()
        except:
           price = None
        info_link = 'https://fptshop.com.vn' + tile.find('a').get("href")
        try:
            img_link = tile.find('img').get("src")
        except:
            img_link = None
        product = {"name": name, 
                   "price": data_standardize_old.get_price(price),
                   "info_link": info_link, 
                   "img_link": img_link, 
                   "shop": "fpt",
                   "brand": data_standardize_old.get_brand(name),
                   "type": type
        }
        product_t = tuple(product.values())
        if product_t[1] == 0 or (product_t[3] == None) or (product_t in products):
            continue
        products.add(product_t)

    end = time.time()
    print("{} {}. {}".format("fpt", len(products) - prev_len, type, end-start))

def scrape_fpt3(driver, products, url):
    start = time.time()
    prev_len = len(products)
    # get the web page
    driver.get(url)
    type = data_standardize_old.get_type_slashslash(url)
    type = data_standardize_old.get_true_type(type)

    # click the button at most 20 times to load more products
    for n in range(40):
        button = driver.find_element(By.CSS_SELECTOR, "body > main > div > div > div.cate-filter > div > div.cate-filter__right > div.flex.flex-center-hor.p-t-12.p-b-16.p-x-16 > a")
        try:
            button.click()
            s = randint(1, 2)
            time.sleep(s * 0.005)
        except:
            break

    

    # page_source is a variable created by Selenium - it holds all the HTML
    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")
    tiles = soup.select("body > main > div > div > div.cate-filter > div > div.cate-filter__right > div.product-grid.product-grid--3.lstproduct > div.product.product__item.product--absolute")

    for tile in tiles:
        try:
            name = tile.find('h3').get_text().strip()
        except:
            continue
        try:
            price = tile.select("div.product__info > div.product__price > div")[0].text.strip()
        except:
           price = None
        info_link = 'https://fptshop.com.vn' + tile.find('a').get("href")
        try:
            img_link = tile.find('img').get("src")
        except:
            img_link = None
        product = {"name": name, 
                   "price": data_standardize_old.get_price(price),
                   "info_link": info_link, 
                   "img_link": img_link, 
                   "shop": "fpt",
                   "brand": data_standardize_old.get_brand(name),
                   "type": type
        }
        product_t = tuple(product.values())
        if (product_t[1] == 0) or (product_t[3] == None) or (product_t in products):
            continue
        products.add(product_t)

    end = time.time()
    print("{} {}. {}".format("fpt", len(products) - prev_len, type, end-start))


def scrape_pvu(driver, products, url):
    start = time.time()
    prev_len = len(products)
    # get the web page
    driver.get(url)
    type = data_standardize_old.get_type_slashslash(url)
    type = data_standardize_old.get_true_type(type)

    # click the button at most 100 times to load more products
    for n in range(100):    

        # page_source is a variable created by Selenium - it holds all the HTML
        page = driver.page_source
        soup = BeautifulSoup(page, "html.parser")
        tiles = soup.find_all('div', class_="css-13w7uog")    

        for tile in tiles:
            name = tile.find('h3').get_text().strip()
            price = tile.find('div', {'class': 'css-1co26wt'}).find('div', {'type': 'subtitle'}).get_text().strip()
            info_link = 'https://phongvu.vn' + tile.find('a').get("href")
            img_link = tile.find('img').get("src")
            brand = tile.find('div', {'class': 'css-68cx5s'}).find('div').get_text().strip().upper()
            product = {"name": name, 
                   "price": data_standardize_old.get_price(price),
                   "info_link": info_link, 
                   "img_link": img_link, 
                   "shop": "pvu",
                   "brand": brand,
                   "type": type
            }
            product_t = tuple(product.values())
            if (product_t[1] == 0) or (product_t[3] == None) or (product_t in products):
                continue
            products.add(product_t)

    

        try:
            button = driver.find_element(By.CSS_SELECTOR, "#__next > div > div > div > div > div:nth-child(4) > div:nth-child(2) > div > div.teko-col.teko-col-10.css-gr7r8o > div.teko-row.css-16rlp3f > div > div > div:last-child")
            button.click()
            s = randint(1, 2)
            #print("--------------------------------------------------------------------------       ", n)
            time.sleep(s * 0.005)
        except:
            break
    end = time.time()
    print("{} {}. {}".format("pvu", len(products) - prev_len, type, end-start))

def scrape_cph(driver, products, url):
    start = time.time()
    prev_len = len(products)
    # get the web page
    driver.get(url)
    type = data_standardize_old.get_type_slashdot(url)
    type = data_standardize_old.get_true_type(type)

    for n in range(50):
        try:
            # handle pop-up
            popup1_close = driver.find_element(By.CLASS_NAME, "model-close is-large")            
            popup1_close.click()
        except:
            try:     
                # handle pop-up
                popup2_close = driver.find_element(By.CLASS_NAME, "cancel-button-top")
                popup2_close.click()
            except NoSuchElementException:
                try:
                    button = driver.find_element(By.CLASS_NAME, "cps-block-content_btn-showmore")
                    button.click()
                    s = randint(1, 2)
                    time.sleep(s * 0.01)        
                except:
                    continue

    # page_source is a variable created by Selenium - it holds all the HTML
    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    tiles = soup.find_all('div', class_="product-info-container product-item")
                
    for tile in tiles:
        name = tile.find('h3').get_text().strip()
        price = tile.find('p', class_="product__price--show").get_text().strip()
        info_link = tile.find('a').get("href")
        img_link = tile.find('img').get("src")
        product = {"name": name, 
                   "price": data_standardize_old.get_price(price),
                   "info_link": info_link, 
                   "img_link": img_link, 
                   "shop": "cph",
                   "brand": data_standardize_old.get_brand(name),
                   "type": type
        }
        product_t = tuple(product.values())
        if (product_t[1] == 0) or (product_t[3] == None) or (product_t in products):
            continue
        products.add(product_t)

    
    end = time.time()
    print("{} {}. {}".format("cph", len(products) - prev_len, type, end-start))

def scrape_tpr(driver, products, url):
    start = time.time()
    prev_len = len(products)

    # get the web page
    driver.get(url)
    type = data_standardize_old.get_type_slash(url)
    type = data_standardize_old.get_true_type(type)

    # click the button at most 20 times to load more products
    for n in range(20):
        try:
            button = driver.find_element(By.XPATH, "//*[@id=\"__layout\"]/div/main/div[3]/div[3]/button")
            button.click()
            #print("---------------------------------------------------OK")
            s = randint(1, 2)
            time.sleep(s * 0.005)
        except:
            break
    
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

    for tile in tiles:
        name = tile.find('div', class_='t-product-item__title').get_text().strip()
        price = tile.find('span', class_='t-product-item__price').get_text()
        info_link = 'https://www.thinkpro.vn' + tile.get("href")
        img_link = tile.find('img').get("data-src")
        product = {"name": name, 
                   "price": data_standardize_old.get_price(price),
                   "info_link": info_link, 
                   "img_link": img_link, 
                   "shop": "tpr",
                   "brand": data_standardize_old.get_brand(name),
                   "type": type
        }
        product_t = tuple(product.values())
        if (product_t[1] == 0) or (product_t[3] == None) or (product_t in products):
            continue
        products.add(product_t)

    
    end = time.time()
    print("{} {}. {}".format("tpr", len(products) - prev_len, type, end-start))


def scrape_laz(driver, products, url):
    start = time.time()
    prev_len = len(products)

    # get the web page
    driver.get(url)
    type = data_standardize_old.get_type_slashdot(url)
    type = data_standardize_old.get_true_type(type)


    # click the button at most 100 times to load more products
    for n in range(100):    
        # page_source is a variable created by Selenium - it holds all the HTML
        src = driver.page_source
        soup = BeautifulSoup(src, "html.parser")
        tiles = soup.select('#product > div')  

        for tile in tiles:
            name = data_standardize_old.get_name_laz(tile.find('a', class_='p-name').get_text().strip())
            if name == None:
                continue
            try:
                price = tile.find('span', class_='show-him').get_text().strip()
            except:
                continue
            info_link = 'https://laptopaz.vn' + tile.find('a').get("href")
            img_link = 'https://laptopaz.vn' + tile.find('img').get("src")
            product = {"name": name, 
                   "price": data_standardize_old.get_price(price), 
                   "info_link": info_link, 
                   "img_link": img_link, 
                   "shop": "laz",
                   "brand": data_standardize_old.get_brand(name),
                   "type": type
            }
            product_t = tuple(product.values())
            if (product_t[1] == 0) or (product_t[3] == None) or (product_t in products):
                continue
            products.add(product_t)

        

        try:
            button = driver.find_element(By.CSS_SELECTOR, "body > main > div.product-list > div > nav > ul > li:last-child")
            if button.text == 'Next':
                button.click()
            else:
                break
            s = randint(1, 2)
            time.sleep(s * 0.005)
        except:
            break
    
    end = time.time()
    print("{} {}. {}".format("laz", len(products) - prev_len, type, end-start))


def scrape_hch(driver, products, url):
    start = time.time()
    prev_len = len(products)
    # get the web page
    driver.get(url)
    type = data_standardize_old.get_type_slash(url)
    type = data_standardize_old.get_true_type(type)

    # click the button at most 100 times to load more products
    for n in range(100):    
        # page_source is a variable created by Selenium - it holds all the HTML
        src = driver.page_source
        soup = BeautifulSoup(src, "html.parser")
        tiles = soup.select('#template-collection > section.section.wrap_background > div > div > div > div > div.category-products.products > div.products-view.products-view-grid.collection_reponsive.list_hover_pro > div.row.product-list.content-col > div')  

        for tile in tiles:
            name = tile.find('h3', class_='product-name').get_text().strip()
            try:    
                price = tile.find('div', class_='price-box').find('span', class_='price').get_text().strip()
            except:
                break
            info_link = 'https://hangchinhhieu.vn' + tile.find('h3', class_='product-name').find('a').get("href")
            img_link = 'https:' + tile.find('img').get("src")
            product = {"name": name, 
                   "price": data_standardize_old.get_price(price), 
                   "info_link": info_link, 
                   "img_link": img_link, 
                   "shop": "hch",
                   "brand": data_standardize_old.get_brand(name),
                   "type": type
            }
            product_t = tuple(product.values())
            if (product_t[1] == 0) or (product_t[3] == None) or (product_t in products):
                continue
            products.add(product_t)


        try:
            button = driver.find_element(By.CSS_SELECTOR, "#template-collection > section.section.wrap_background > div > div > div > div > div.category-products.products > div.products-view.products-view-grid.collection_reponsive.list_hover_pro > div.section.pagenav > nav > ul > li:last-child")
            button.click()
            s = randint(1, 2)
            time.sleep(s * 0.005)
        except:
            break

        
    end = time.time()
    print("{} {}. {}".format("hch", len(products) - prev_len, type, end-start))



def scrape_pvu2(driver, products, url):
    start = time.time()
    prev_len = len(products)
    # get the web page
    driver.get(url)
    type = data_standardize_old.get_type_slashslash(url)
    type = data_standardize_old.get_true_type(type)

    # click the button at most 100 times to load more products
    for n in range(100):    

        # page_source is a variable created by Selenium - it holds all the HTML
        page = driver.page_source
        soup = BeautifulSoup(page, "html.parser")
        tiles = soup.find_all('div', class_="css-13w7uog")    

        for tile in tiles:
            
            info_link = 'https://phongvu.vn' + tile.find('a').get("href")
            driver.get(info_link)

            img_link = tile.select('#__next > div > div > div > div > div:nth-child(4) > div > div > div:nth-child(2) > div.css-1hwtax5 > div > div > div.css-1i1dodm > div:nth-child(1) > div.productDetailPreview > div > img')
            name = tile.select('#__next > div > div > div > div > div:nth-child(4) > div > div > div:nth-child(2) > div.css-1hwtax5 > div > div > div.css-1i1dodm > div.css-17aam1')[0].get_text()

            # name = tile.find('h3').get_text().strip()
            # price = tile.find('div', {'class': 'css-1co26wt'}).find('div', {'type': 'subtitle'}).get_text().strip()
            # img_link = tile.find('img').get("src")
            # brand = tile.find('div', {'class': 'css-68cx5s'}).find('div').get_text().strip().upper()
            # product = {"name": name, 
            #        "price": data_standardize.get_price(price),
            #        "info_link": info_link, 
            #        "img_link": img_link, 
            #        "shop": "pvu",
            #        "brand": brand,
            #        "type": type
            # }
            product = {"info_link": info_link, "img_link": img_link}
            product_t = tuple(product.values())
            # if (product_t[1] == 0) or (product_t[3] == None) or (product_t in products):
            # if (product_t in products):
            #     continue
            # products.add(product_t)
            print(name, info_link)

    

        try:
            button = driver.find_element(By.CSS_SELECTOR, "#__next > div > div > div > div > div:nth-child(4) > div:nth-child(2) > div > div.teko-col.teko-col-10.css-gr7r8o > div.teko-row.css-16rlp3f > div > div > div:last-child")
            button.click()
            s = randint(1, 2)
            #print("--------------------------------------------------------------------------       ", n)
            time.sleep(s * 0.005)
        except:
            break
    end = time.time()
    print("{} {}. {}".format("pvu", len(products) - prev_len, type, end-start))