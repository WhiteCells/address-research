import pymysql
from app.config import DBConfig
import os



db_config = {
    'host': DBConfig.HOST,  # 例如：'localhost'
    'user': DBConfig.USER,  # 您的数据库用户名
    'password': DBConfig.PASSWORD,  # 您的数据库密码
    'database': DBConfig.DATABASE,  # 您的数据库名
    'charset': 'utf8mb4',  # 字符编码
    'cursorclass': pymysql.cursors.DictCursor  # 使用字典游标
}



def amap_address(filepath,rank):
    table_name = DBConfig.DATATABLE+""+rank

    sql = f"""
    INSERT INTO `{table_name}`
    (address, ocr_address, province, city, district, level, location, township)
    VALUES (%s, %s, %s, %s, %s, %s, %s ,%s);
    """
    with open(filepath, 'r', encoding='utf-8') as f:
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
            township:
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
            township = address_components[8].split(':')[1]

            print(formatted_address)
            print(ocr_address)
            print(province)
            print(city)
            print(district)
            print(level)
            print(location)
            print(township)

            data = (formatted_address, ocr_address, province, city, district, level, location, township)

            with connection.cursor() as cursor:
                cursor.execute(sql, data)
                connection.commit()

     except Exception as e:
        print(e)

     finally:
        if connection:
            connection.close()
            print("数据库连接已关闭")

def process_res_amap_dir():
  for root, dirs, files in os.walk(DBConfig.INPUT_PATH):
    for file in files:
        if not file.endswith(".txt"):
            continue

        file_path = os.path.join(root, file)
        print('=> processing: ', file_path)

        # 取出文件名（不包含后缀）
        filename = os.path.basename(file_path).split('.')[0]
        # 取出地图等级
        rank = filename.split('_')[-1]
        amap_address(file_path, rank)

