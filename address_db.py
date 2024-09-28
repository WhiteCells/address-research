import pymysql

file = 'belong_jx5.txt'

db_config = {
    'host': '192.168.10.59',  # 例如：'localhost'
    'user': 'research',  # 您的数据库用户名
    'password': '6usKz1Pi8aQ7q8WL',  # 您的数据库密码
    'database': 'address-research-mater',  # 您的数据库名
    'charset': 'utf8mb4',  # 字符编码 
    'cursorclass': pymysql.cursors.DictCursor  # 使用字典游标
}

table_name = 'jx_amap_address'

sql = f"""
INSERT INTO `{table_name}`
(address, ocr_address, province, city, district, level, location)
VALUES (%s, %s, %s, %s, %s, %s, %s);
"""

with open(file, 'r', encoding='utf-8') as f:
    try:
        connection = pymysql.connect(**db_config)
        print('连接到数据库')
        for line in f:
            address_components = line.strip().split(',')
            """
            formatted_address:湖北省武汉市江夏区烽火科技,
            ocr_address:烽火科技,
            province:湖北省,
            city:武汉市,
            district:江夏区,
            level:住宅区,
            location:114.424248,
            30.447127
            """
            formatted_address = address_components[0].split(':')[1]
            ocr_address = address_components[1].split(':')[1]
            province = address_components[2].split(':')[1]
            city = address_components[3].split(':')[1]
            district = address_components[4].split(':')[1]
            level = address_components[5].split(':')[1]
            location1 = address_components[6].split(':')[1]
            location2 = address_components[7]
            location = location1 + ',' + location2
            
            print(formatted_address)
            print(ocr_address)
            print(province)
            print(city)
            print(district)
            print(level)
            print(location)

            data = (formatted_address, ocr_address, province, city, district, level, location)

            with connection.cursor() as cursor:
                cursor.execute(sql, data)
                connection.commit()

    except Exception as e:
        print(e)
    
    finally:
        if connection:
            connection.close()
            print("数据库连接已关闭")
