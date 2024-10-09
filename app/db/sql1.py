import re
import mysql.connector
from mysql.connector import Error
from app.config
# 数据库连接配置
config = {
    'user': 'research',
    'password': '6usKz1Pi8aQ7q8WL',
    'host': '192.168.10.59',
    'database': 'address-research-mater',
    'raise_on_warnings': True
}

# 读取文本文档
def read_data_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return lines

# 解析每一行数据
def parse_line(line):
    pattern = r"text: (.*?),confidence: (.*?),text_box_position: (\[\[\d+,\s\d+\],\s\[\d+,\s\d+\],\s\[\d+,\s\d+\],\s\[\d+,\s\d+\]\])"
    match = re.match(pattern, line)
    if match:
        text = match.group(1)
        confidence = float(match.group(2))
        text_box_position = eval(match.group(3))
        return text, confidence, text_box_position
    return None

# 插入数据到数据库
def insert_data_to_db(data, connection):
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO ocr_results (text, confidence, text_box_position)
    VALUES (%s, %s, %s)
    """
    for item in data:
        if item:
            text, confidence, text_box_position = item
            cursor.execute(insert_query, (text, confidence, str(text_box_position)))
    connection.commit()
    cursor.close()

# 主函数
def main():
    file_path = 'newdemo_z63.txt'
    lines = read_data_from_file(file_path)
    parsed_data = [parse_line(line) for line in lines]

    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Connected to MySQL Server version {db_info}")
            insert_data_to_db(parsed_data, connection)
            print("Data inserted successfully.")
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    main()