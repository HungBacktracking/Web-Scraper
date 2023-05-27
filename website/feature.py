import mysql.connector
from flask import render_template
from gifts import *
import config


def get_parameters(table_name):
    db = mysql.connector.connect(
        host = "aws.connect.psdb.cloud",
        user = config.USER,
        password = config.PASSWORD,
        database = "products" 
    )
    cursor = db.cursor()

    cursor.execute(f"""
    SELECT COLUMN_NAME 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_NAME = '{table_name}'""")
    parameter_names = cursor.fetchall()

    parameters = []
    for row in parameter_names:
        parameter_name = str(row[0])
        if parameter_name.lower() in ["name", "info_link", "id", "img_link", 'gpu', 'type', 'shop']:
            continue

        parameter = {
            "name": beautifyName[str(parameter_name)],
            "values": []
        }


        flag = False
        if parameter_name == "brand" or parameter_name == "screen":
            cursor.execute(f"""
            SELECT DISTINCT {parameter_name}
            FROM {table_name}
            WHERE {parameter_name} IS NOT NULL
            """)
            data = cursor.fetchall()

            for row in data:
                for value in str(row[0]).split(', '):
                    if parameter_name.lower() in ["screen"]:
                            if float(value) < 10.0:
                                continue
                            if float(value) >= 40.0:
                                flag = True
                                continue
                            parameter["values"].append(value.strip() + ' inch')
                    else:
                        parameter["values"].append(value.strip())
        else:
            for value in parameterValue[parameter_name]:
                parameter["values"].append(value.strip())

        if parameter_name != "price" and parameter_name != "screen": parameter["values"].append("Khác")
        if parameter_name == "screen": 
            parameter["values"].sort()
            if flag == True:
                parameter["values"].append("40 inch+")
        
        parameters.append(parameter)
    
    return parameters


def createSQL(table_name, filters, sort_type):
    select = "SELECT name, price, info_link, img_link, shop" + selectFilter[table_name] + ", id "
    sql = select + f""" 
        FROM {table_name} 
        WHERE name IS NOT NULL 
        AND price IS NOT NULL 
        AND info_link IS NOT NULL 
        AND img_link IS NOT NULL """

    # loop through all filters
    condition_sql = []
    filter_choices = []
    for filter_name, filter  in filters.items():
        if not filter:
            continue

        condition_in_filter = []
        filter_name = convertNameDB(filter_name)

        for requiredment in filter:
            requiredment = str(requiredment)
            if filter_name == 'ram' and requiredment.lower() != 'khác':
                requiredment = extract_ram(requiredment)
            if filter_name == 'screen' and requiredment.lower() != 'khác':
                requiredment = extract_screen(requiredment)
            if filter_name == 'refresh_rate' and requiredment.lower() != 'khác':
                requiredment = extract_refresh_rate(requiredment)
            if filter_name == 'cpu' and requiredment.lower() != 'khác':
                requiredment = extract_cpu(requiredment)
            
            if filter_name == "screen" and requiredment == "40":
                value = findTwoNumber(requiredment)
                condition_in_filter.append(f"{str(filter_name)} >= {float(value) / 1000000}")
                continue
            elif filter_name == "price":
                if "Dưới" in requiredment:
                    value = findTwoNumber(requiredment)
                    condition_in_filter.append(f"{str(filter_name)} < {value}")
                    continue

                if "Trên" in requiredment:
                    value = findTwoNumber(requiredment)
                    condition_in_filter.append(f"{str(filter_name)} > {value}")
                    continue

                min, max = findTwoNumber(requiredment)
                condition_in_filter.append(f"{str(filter_name)} BETWEEN {min} AND {max}")

            elif requiredment.lower() != 'khác':
                if filter_name == 'screen' and requiredment[len(requiredment) - 1] == '0':
                    condition_in_filter.append(f"{str(filter_name)} LIKE %s")
                    filter_choices.append(f"%{requiredment[:-2]}%")
                condition_in_filter.append(f"{str(filter_name)} LIKE %s")
                filter_choices.append(f"%{requiredment}%")

            else:
                condition_in_filter.append(f"{str(filter_name)} IS NULL ")
                if filter_name == 'disk_storage':
                    condition_in_filter.append(f"{str(filter_name)} LIKE %s")
                    filter_choices.append(f"%240GB%")
                    condition_in_filter.append(f"{str(filter_name)} LIKE %s")
                    filter_choices.append(f"%250GB%")
                    condition_in_filter.append(f"{str(filter_name)} LIKE %s")
                    filter_choices.append(f"%500GB%")
                    condition_in_filter.append(f"{str(filter_name)} LIKE %s")
                    filter_choices.append(f"%510GB%")

        condition_sql.append(f'({" OR ".join(condition_in_filter)})')

    if condition_sql:
        sql += "AND" + " AND ".join(condition_sql)

    if sort_type == 3:
        sql += " ORDER BY price"
    elif sort_type == 2:
        sql += " ORDER BY price DESC"

    return sql, filter_choices


def filter_product(table_name: str, filters = {}, page_index: int = 1, product_per_page: int = 20, sort_type: int = 1):
    db = mysql.connector.connect(
        host = "aws.connect.psdb.cloud",
        user = config.USER,
        password = config.PASSWORD,
        database = "products" 
    )
    cursor = db.cursor()

    if not page_index or page_index < 1:
        page_index = 1
    if not product_per_page or product_per_page < 0:
        product_per_page = 20
    if not filters:
        filters = {}
    if sort_type not in [1, 2, 3]:
        sort_type = 1
    

    sql, filter_choices = createSQL(table_name, filters, sort_type)
    cursor.execute(sql, filter_choices)
    rows = cursor.fetchall()

    product_info = {
        "total": len(rows),
        "category": table_name,
        "sort": None,
        "listproduct": None,
        "pagination": None,
    }

    start_index = min(len(rows), (page_index - 1) * product_per_page)
    end_index = min(len(rows), start_index + product_per_page)

    # tính tổng số trang
    total_pages = len(rows) // product_per_page + (1 if len(rows) % product_per_page > 0 else 0)

    if page_index == total_pages and len(rows) % product_per_page != 0:
        end_index = start_index + len(rows) % product_per_page

    
    sort = {
        "table_name": table_name,
        "current_sort": sort_type,
        "sortList": sortList,
    }

    listproduct = []
    for row in rows[start_index:end_index]:
        product = {
            "table_name": table_name,
            "product_name": row[0],
            "price": '{:0,}'.format(row[1]).replace(",", ".") + "đ", 
            "info_link": row[2],
            "img_link": row[3],
            "shop": row[4],
        }
        if table_name == 'Laptop':
            product["screen"] = row[5]
            product["cpu"] = row[6]
            product["ram"] = row[7]
            product["disk_type"] = row[8]
            product["disk_storage"] = row[9]
            product["gpu"] = row[10]
            product["id"] = row[11]
        elif table_name == 'PC':
            product["cpu"] = row[5]
            product["ram"] = row[6]
            product["disk_type"] = row[7]
            product["disk_storage"] = row[8]
            product["id"] = row[9]
        elif table_name == 'Screen':
            product["screen"] = row[5]
            product["refresh_rate"] = row[6]
            product["id"] = row[7]
        else: product["id"] = row[5]
        listproduct.append(product)

    pagination = {
        "table_name": table_name,
        "current_sort": sort_type,
        "current_page": page_index,
        "total_pages": total_pages,
    }


    product_info["sort"] = render_template("sort.html", sort = sort)
    product_info["listproduct"] = render_template("listproduct.html", listproduct = listproduct, table_name = table_name)
    product_info["pagination"] = render_template("pagination.html", pagination = pagination)
    return product_info



def findProductById(table_name: str, index: str):
    db = mysql.connector.connect(
        host = "aws.connect.psdb.cloud",
        user = config.USER,
        password = config.PASSWORD,
        database = "products" 
    )
    cursor = db.cursor()

    select = "SELECT name, price, info_link, img_link, shop" + selectFilter[table_name] + ", brand "
    sql = select + f""" 
        FROM {table_name} 
        WHERE name IS NOT NULL 
        AND price IS NOT NULL 
        AND info_link IS NOT NULL 
        AND img_link IS NOT NULL 
        AND id = {index} """
    cursor.execute(sql)
    row = cursor.fetchone()

    product = {
        "product_name": row[0],
        "price": '{:0,}'.format(row[1]).replace(",", ".") + "đ", 
        "info_link": row[2],
        "img_link": row[3],
        "shop": row[4],
    }

    conditional = ""
    if table_name == 'Laptop':
        product["screen"] = row[5]
        if product["screen"] != 'null' and product["screen"] != None: conditional = conditional + f" AND screen = {product['screen']} "
        product["cpu"] = row[6]
        if product["cpu"] != 'null' and product["cpu"] != None: conditional = conditional + f" AND cpu LIKE '%{product['cpu']}%' "
        product["ram"] = row[7]
        if product["ram"] != 'null' and product["ram"] != None: conditional = conditional + f" AND ram = {product['ram']} "
        product["disk_type"] = row[8]
        if product["disk_type"] != 'null' and product["disk_type"] != None: conditional = conditional + f" AND disk_type LIKE '%{product['disk_type']}%' "
        product["disk_storage"] = row[9]
        if product["disk_storage"] != 'null' and product["disk_storage"] != None: conditional = conditional + f" AND disk_storage LIKE '%{product['disk_storage']}%' "
        product["gpu"] = row[10]
        product["brand"] = row[11]
    elif table_name == 'PC':
        product["cpu"] = row[5]
        if product["cpu"] != 'null' and product["cpu"] != None: conditional = conditional + f" AND cpu LIKE '%{product['cpu']}%' "
        product["ram"] = row[6]
        if product["ram"] != 'null' and product["ram"] != None: conditional = conditional + f" AND ram = {product['ram']} "
        product["disk_type"] = row[7]
        if product["disk_type"] != 'null' and product["disk_type"] != None: conditional = conditional + f" AND disk_type LIKE '%{product['disk_type']}%' "
        product["disk_storage"] = row[8]
        if product["disk_storage"] != 'null' and product["disk_storage"] != None: conditional = conditional + f" AND disk_storage LIKE '%{product['disk_storage']} %' "
        product["brand"] = row[9]
    elif table_name == 'Screen':
        product["screen"] = row[5]
        if product["screen"] != 'null' and product["screen"] != None: conditional = conditional + f" AND screen = {product['screen']} "
        product["refresh_rate"] = row[6]
        if product["refresh_rate"] != 'null' and product["refresh_rate"] != None: conditional = conditional + f" AND refresh_rate = {product['refresh_rate']} "
        product["brand"] = row[7]
    else: 
        product["brand"] = row[5]
    tmp = cleanData(product["product_name"])

    against = ""
    for i in range(len(tmp)):
        if tmp == '' or tmp == ' ':
            continue
        if i + 1 == len(tmp):
            against = against + str(tmp[i])
        else:
            against = against + str(tmp[i]) + ","
    if against.endswith(','):
        against = against[:-1]

    # Xóa một trong hai dấu ',' liên tiếp nhau
    against = re.sub(r',,', ',', against)
    

    select = "SELECT name, price, info_link, img_link, shop" + selectFilter[table_name]
    sql = select + f""" 
        FROM {table_name} 
        WHERE name IS NOT NULL 
        AND price IS NOT NULL 
        AND info_link IS NOT NULL 
        AND img_link IS NOT NULL 
        AND id <> {index}  
        AND brand LIKE  '%{product['brand']}%' """ + conditional + f""" 
        AND MATCH(name) AGAINST('{against}') 
        LIMIT 15 """
    cursor.execute(sql)
    rows = cursor.fetchall()

    check = {
        "tgd": False,
        "pvu": False,
        "tpr": False,
        "fpt": False,
    }
    listproduct = []
    for row in rows:
        if check[row[4]] == True:
            continue
        check[row[4]] = True

        product_ = {
            "product_name": row[0],
            "price": '{:0,}'.format(row[1]).replace(",", ".") + "đ", 
            "info_link": row[2],
            "img_link": row[3],
            "shop": row[4],
        }
        if table_name == 'Laptop':
            product_["screen"] = row[5]
            product_["cpu"] = row[6]
            product_["ram"] = row[7]
            product_["disk_type"] = row[8]
            product_["disk_storage"] = row[9]
            product_["gpu"] = row[10]
        elif table_name == 'PC':
            product_["cpu"] = row[5]
            product_["ram"] = row[6]
            product_["disk_type"] = row[7]
            product_["disk_storage"] = row[8]
        elif table_name == 'Screen':
            product_["screen"] = row[5]
            product_["refresh_rate"] = row[6]
        listproduct.append(product_)

    return product, listproduct




def search_product(name: str,  page_index: int = 1, product_per_page: int = 20, sort_type: int = 1):
    db = mysql.connector.connect(
        host = "aws.connect.psdb.cloud",
        user = config.USER,
        password = config.PASSWORD,
        database = "products" 
    )
    cursor = db.cursor()
    if name == None:
        name = ""

    if not page_index or page_index < 1:
        page_index = 1
    if not product_per_page or product_per_page < 0:
        product_per_page = 20
    if sort_type not in [1, 2, 3]:
        sort_type = 1

    cursor.execute("SHOW TABLES")
    rows = cursor.fetchall()
    basic_info_sql_cmd = []
    for row in rows:
        if row[0] not in allow_path:
            continue
        basic_info_sql_cmd.append(f"""
        (SELECT '{row[0]}' AS table_name, name, price, info_link, img_link, shop """ + selectFilterAll[row[0]] + f""", id 
        FROM {row[0]})
        """)
    search_table_sql = " UNION ".join(basic_info_sql_cmd)

    search_sql = f"""
    SELECT *
    FROM ({search_table_sql}) AS R
    WHERE name LIKE %s 
    AND price IS NOT NULL 
    AND img_link IS NOT NULL 
    AND info_link IS NOT NULL 
    """

    if sort_type == 3:
        search_sql += " ORDER BY price "
    elif sort_type == 2:
        search_sql += " ORDER BY price DESC "
    
    cursor.execute(search_sql, ['%' + name.replace(' ', '%') + '%'])
    rows = cursor.fetchall()

    product_info = {
        "total": len(rows),
        "category": "Search",
        "sort": None,
        "listproduct": None,
        "pagination": None,
    }
    start_index = min(len(rows), (page_index - 1) * product_per_page)
    end_index = min(len(rows), start_index + product_per_page)

    # tính tổng số trang
    total_pages = len(rows) // product_per_page + (1 if len(rows) % product_per_page > 0 else 0)

    if page_index == total_pages and len(rows) % product_per_page != 0:
        end_index = start_index + len(rows) % product_per_page

    sort = {
        "table_name": "Search",
        "current_sort": sort_type,
        "sortList": sortList,
    }

    listproduct = []
    for row in rows[start_index:end_index]:
        
        product = {
            "table_name": row[0],
            "product_name": row[1],
            "price": '{:0,}'.format(row[2]).replace(",", ".") + "đ", 
            "info_link": row[3],
            "img_link": row[4],
            "shop": row[5],
        }
        if row[0] == 'Laptop':
            product["screen"] = row[6]
            product["cpu"] = row[7]
            product["ram"] = row[8]
            product["disk_type"] = row[9]
            product["disk_storage"] = row[10]
            product["gpu"] = row[11]
            product["id"] = row[13]
        elif row[0] == 'PC':
            product["cpu"] = row[7]
            product["ram"] = row[8]
            product["disk_type"] = row[9]
            product["disk_storage"] = row[10]
            product["id"] = row[13]
        elif row[0] == 'Screen':
            product["screen"] = row[6]
            product["refresh_rate"] = row[12]
            product["id"] = row[13]
        else: product["id"] = row[13]
        listproduct.append(product)
    
    
    pagination = {
        "table_name": "Search",
        "current_sort": sort_type,
        "current_page": page_index,
        "total_pages": total_pages,
    }

    product_info["sort"] = render_template("sort.html", sort = sort)
    product_info["listproduct"] = render_template("listproduct.html", listproduct = listproduct, table_name = "Search")
    product_info["pagination"] = render_template("pagination.html", pagination = pagination)

    return product_info
