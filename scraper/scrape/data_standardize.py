import regex as re

def extract_disk(disk):
    disk = str(disk)
    # if disk == None or disk == '':
    #     return (None, None)
    # in_bracket = re.search(r'\(.*\)', disk)
    # if in_bracket:
    #     disk = disk.replace(in_bracket.group(), "")
    disk_type = re.search(r'SSD|HDD|EMMC', disk.upper())
    if disk_type:
        disk_type = disk_type.group()
    else:
        disk_type = "SSD"
    
    pattern = r'(?<=(SSD|HDD|EMMC))(\s+)?\d+(\s+)?(G|T)B'
    amount = re.search(pattern, disk.upper())
    if amount:
        amount = amount.group()
        if amount == None:
            return (None, None)
        amount = amount.replace(' ', '')
        return (disk_type, amount)
    
    pattern = r'\d+(\s+)?(G|T)B(?=(\s+)?(SSD|HDD|EMMC))'
    amount = re.search(pattern, disk.upper())
    if amount:
        amount = amount.group()
        # amount = normalize_disk_amount(amount)
        if amount == None:
            return (None, None)
        amount = amount.replace(' ', '')
        return (disk_type, amount)
    
    pattern = r'\d+\s*(G|T)B'
    amount = re.search(pattern, disk.upper())
    if amount:
        amount = amount.group()
        # amount = normalize_disk_amount(amount)
        if amount == None:
            return None
        amount = amount.replace(' ', '')
        return (disk_type, amount)
    
    return (None, None)

def extract_screen(screen):
    screen = str(screen)
    if screen == None or screen == '':
        return None
    pattern = r'\d+(\.\d+)?(?=\s*(inch|\'|\"|(\'\')))'
    result = re.search(r'\d+(\.\d+)?(?=\s*(inch|\'|\"|(\'\')))', screen)
    if result:
        result = result.group()
        return float(result)
    
    return None

def extract_ram(data):
    tmp = " " + str(data)
    if data == None or data == '':
        return None
    
    # in_bracket = re.search(r'\(.*\)', data)
    # if in_bracket:
    #     data = data.replace(in_bracket.group(), "")

    pattern = r'(?<=\s)((\d\d)|(\d))(?=(\s*)?GB)'
    amount = re.search(pattern, tmp.upper())
    if amount:
        return int(amount.group())
    return None

def price_to_int(price):
    price = str(price)
    if price: 
        price = re.sub(r"\D", "", price)
        if price == '':
            price = None
        else:
            price = int(price)
        return price
    return None
    
def extract_cpu(text):
    text = str(text)
    text = text.upper()

    # lấy kết quả từ regex
    intel_match = re.search(r'I[3579]', text.upper())
    apple_match = re.search(r'M[12]', text.upper())
    amd_match = re.search(r'(R[3579]|RYZEN\s+[3579])', text.upper())
    celeron_pentium_match = re.search(r'CELERON|PENTIUM', text.upper())

    # trả về kết quả tương ứng nếu match được regex
    if intel_match:
        return intel_match.group().lower()
    elif apple_match:
        return apple_match.group()
    elif amd_match:
        result = amd_match.group()
        if 'RYZEN' in result:
            return 'R' + result[len(result) - 1]
        return result
    elif celeron_pentium_match:
        return celeron_pentium_match.group().lower()

    # nếu không match được regex nào, trả về None
    return None

def extract_refresh_rate(data):
    data = str(data)
    result = re.search(r'\d+(?=\s*Hz)', data)
    if result:
        result = result.group()
        return int(result)
    
    return None

def extract_brand(name):
    name = name.upper()
    brands = ['LENOVO', 'ACER', 'ASUS', 'DELL', 'HP', 'APPLE', 'MSI', 'MICROSOFT', 'ITEL', 'CHUWI', 'LG', 'SONY',
              'AMD', 'LOGITECH', 'TP-LINK', 'TENDA', 'TOTOLINK', 'MERCUSYS', 'XIAOMI', 'EPSON', 'SAMSUNG', 'SANDISK',
              'GIGABYTE', 'XIGMATEK', 'KINGSTON', 'PROLINK', 'CORSAIR', 'ZADEZ', 'RAPOO', 'AOC', 'VIEWSONIC', 'PHILIPS',
              u'PHONG VŨ', 'ASROCK', 'GENIUS', 'RAZER', 'HYPERX', 'A4TECH', 'DAREU', 'E-POWER']
    if 'MACBOOK' in name or 'MAC' in name or 'IMAC' in name:
        return 'APPLE'
    elif 'SURFACE' in name:
        return 'MICROSOFT'
    for brand in brands:
        if brand in name:
            return brand
    return None