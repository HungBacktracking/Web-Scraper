import regex as re

allow_path = [
    'Laptop',
    'PC',
    'Screen',
    'Keyboard',
    'Mouse',
]

sortList = [
    "None",
    "Nổi bật nhất",
    "Giá cao đến thấp",
    "Giá thấp đến cao"
]

NAME = {
    "Laptop": "Laptop",
    "Screen": "Màn hình",
    "PC": "PC",
    "Keyboard": "Bàn phím",
    "Mouse": "Chuột máy tính",
}

DESCRIPTION = {
    "Laptop": "Laptop là một thiết bị máy tính có kích thước nhỏ gọn và di động. Nó được thiết kế để sử dụng trong các hoạt động làm việc, giải trí hoặc học tập khi di chuyển mà không cần phải sử dụng những chiếc máy tính để bàn cồng kềnh.",
    "Screen": "Màn hình máy tính (Computer display, Visual display unit hay Monitor) là thiết bị điện tử dùng để kết nối với máy tính nhằm mục đích hiển thị và phục vụ cho quá trình giao tiếp giữa người sử dụng với máy tính.",
    "PC": "PC là một máy tính cá nhân được thiết kế để sử dụng thường xuyên tại một vị trí duy nhất trên bàn do kích thước và yêu cầu về điện năng tiêu thụ.",
    "Keyboard": "Bàn phím là một thiết bị đầu vào cho máy tính, được sử dụng để nhập dữ liệu và điều khiển các chức năng của máy tính. Bàn phím bao gồm một loạt các phím nhấn, các phím chữ, số, các ký tự đặc biệt và các phím chức năng để thực hiện các tác vụ.",
    "Mouse": "Chuột máy tính một thiết bị ngoại vi được sử dụng để điều khiển con trỏ trên màn hình máy tính và thực hiện các thao tác trên giao diện đồ họa. Chuột thông thường được thiết kế nhỏ gọn, có hai, ba hoặc nhiều nút nhấn với bánh xe cuộn được đặt giữa hai nút.",
}

SHOP = {
    "pvu": "Phong Vũ",
    "tgd": "Thế giới di động",
    "tpr": "ThinkPro",
    "fpt": "FPT Shop",
}


beautifyName = {
    "price": "Khoảng giá",
    "brand": "Thương hiệu",
    "cpu": "CPU",
    "ram": "RAM",
    "disk_type": "Loại ổ cứng",
    "disk_storage": "Dung lượng",
    "screen": "Màn hình",
    "refresh_rate": "Tần số quét",
    "resolution": "Độ phân giải",
}

parameterValue = {
    "price": ["Dưới 5tr", "Từ 5tr đến 10tr", "Từ 10tr đến 15tr", "Từ 15tr đến 20tr", "Trên 20tr"],
    "cpu": ["Intel Core i3", "Intel Core i5", "Intel Core i7", "Intel Core i9", "Intel Celeron", "Intel Pentium", "AMD Ryzen 3", "AMD Ryzen 5", "AMD Ryzen 7", "AMD Ryzen 9", "Apple M1", "Apple M2"],
    "ram": ["4GB", "8GB", "16GB", "32GB", "64GB"],
    "disk_type": ["HDD", "SSD", "EMMC"],
    "disk_storage": ["128GB", "256GB", "512GB", "1TB", "2TB"],
    "refresh_rate": ["60 Hz", "75 Hz", "144 Hz", "165 Hz", "240 Hz"],
    "resolution": ["HD", "Full HD", "2K", "4K"],
}

selectFilter = {
    "Laptop": ", screen, cpu, ram, disk_type, disk_storage, gpu ",
    "PC": ", cpu, ram, disk_type, disk_storage ",
    "Screen": ", screen, refresh_rate ",
    "Keyboard": " ",
    "Mouse": " ",
}

selectFilterAll = {
    "Laptop": ", screen, cpu, ram, disk_type, disk_storage, gpu, NULL AS refresh_rate ",
    "PC": ", NULL AS screen, cpu, ram, disk_type, disk_storage, NULL AS gpu, NULL AS refresh_rate ",
    "Screen": ", screen, NULL AS cpu, NULL AS ram, NULL AS disk_type, NULL AS disk_storage, NULL AS gpu, refresh_rate ",
    "Keyboard": ", NULL AS screen, NULL AS cpu, NULL AS ram, NULL AS disk_type, NULL AS disk_storage, NULL AS gpu, NULL AS refresh_rate ",
    "Mouse": ", NULL AS screen, NULL AS cpu, NULL AS ram, NULL AS disk_type, NULL AS disk_storage, NULL AS gpu, NULL AS refresh_rate ",
}

def cleanData(data):
    tmp = str(data)
    tmp = tmp.replace("(", " ")
    tmp = tmp.replace(")", " ")
    tmp = tmp.replace("-", " ")
    tmp = tmp.replace(",", " ")
    tmp = tmp.replace("'", " ")
    tmp = tmp.replace('"', ' ')
    tmp = tmp.replace("/", " ")
    tmp = tmp.split(" ")

    return tmp

def extract_screen(screen):
    screen = str(screen)
    if screen == None or screen == '':
        return None
    result = re.search(r'\d+(\.\d+)?(?=\s*(inch|\'|\"|(\'\')))', screen)
    if result:
        result = result.group()
        return str(result)
    
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
        return str(amount.group())
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
        return str(result)
    
    return None


def convertNameDB(value):
    key = next((k for k, v in beautifyName.items() if v == value), None)
    return key

def findTwoNumber(data):
    data = str(data)
    pattern = r'(?=\s*)\d+'
    matches = re.findall(pattern, data)
    
    if (len(matches) < 2): return int(matches[0]) * 1000000
    return int(matches[0]) * 1000000, int(matches[1]) * 1000000