import pymysql
import os


db_config = {
    'host': '192.168.10.59',
    'user': 'research',
    'password': '6usKz1Pi8aQ7q8WL',
    'database': 'address-research-mater',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# db_config = {
#     'host': '127.0.0.1',
#     'user': 'root',
#     'password': '10101',
#     'database': 'address-research-mater',
#     'charset': 'utf8mb4',
#     'cursorclass': pymysql.cursors.DictCursor
# }

"""
- 小区名（目录）
    - 栋名（文件）
        - 栋号 单元 层数 室号 室号 室号 室号
    - 栋名
        - 栋号 单元 层数 室号 室号
"""

"""
CREATE TABLE jx_community (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '小区 id',
    name VARCHAR(255) NOT NULL COMMENT '小区名'
) COMMENT '江夏小区';

CREATE TABLE jx_c_building (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '栋 id',
    community_id VARCHAR(255) COMMENT '小区 id',
    name VARCHAR(255) NOT NULL COMMENT '栋名',
    FOREIGN KEY (community_id) REFERENCES jx_community(id)
) COMMENT '江夏小区栋';

CREATE TABLE jx_cb_room (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '室 id',
    building_id VARCHAR(255) COMMENT '栋 id',
    building_number VARCHAR(50) COMMENT '栋号',
    unit VARCHAR(255) COMMENT '单元',
    floor VARCHAR(255) COMMENT '楼层',
    number VARCHAR(50) COMMENT '室号',
    FOREIGN KEY (building_id) REFERENCES jx_c_building(id)
) COMMENT '江夏小区栋室';

INSERT INTO Community (name) VALUES ('小区A');

INSERT INTO Building (community_id, name, building_number)
VALUES (1, '栋1', '001');

INSERT INTO Room (building_id, unit, floor, number)
VALUES (1, '101', '1', '101'), (1, '101', '1', '102');

# 2
CREATE TABLE jx_community (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '室 id',
    community_name VARCHAR(255) NOT NULL COMMENT '小区名',
    building_name VARCHAR(255) NOT NULL COMMENT '栋名',
    building_number VARCHAR(50) COMMENT '栋号',
    unit VARCHAR(255) COMMENT '单元',
    floor VARCHAR(255) COMMENT '楼层',
    number VARCHAR(50) COMMENT '室号',
    FOREIGN KEY (building_id) REFERENCES jx_c_building(id)
) COMMENT '武汉市江夏区小区';


    data = (formatted_address, ocr_address, province, city, district, level, location)

    with connection.cursor() as cursor:
        cursor.execute(sql, data)
        connection.commit()

"""

# jx_community_table_name = 'jx_community'
# jx_c_building_table_name = 'jx_c_building'
# jx_cb_room_table_name = 'jx_cb_room'

# commnuity_sql = f"""
# INSERT INTO {jx_community_table_name} (name)
# VALUES (%s);
# """

# building_sql = f"""
# INSERT INTO {jx_c_building_table_name} (community_id, name, building_number)
# VALUES (%s, %s, %s);
# """

# room_sql = f"""
# INSERT INTO {jx_cb_room_table_name} (building_id, unit, floor, number)
# VALUES (%s, %s, %s, %s);
# """

# current
jx_community_table_name = 'jx_community'

sql = f"""
INSERT INTO {jx_community_table_name} (community_name, building_name, building_number, unit, floor, number)
VALUES (%s, %s, %s, %s, %s, %s);
"""

def connect_db():
    try:
        return pymysql.connect(**db_config)
    except Exception as e:
        print(e)
        return None

community_name_path = 'jx_community'



if __name__ == '__main__':
    connection = connect_db()

    for community_name in os.listdir(community_name_path):
        print(community_name)
        building_name_path = os.path.join(community_name_path, community_name)
        
        for building_name in os.listdir(building_name_path):
            print(building_name)
            room_name_path = os.path.join(building_name_path, building_name)
            building_name = os.path.splitext(building_name)[0]
            print('===> building name: ', building_name)
            with open(room_name_path, 'r', encoding='utf-8') as f:
                content = f.read()

            one_line_flag = True
            
            for line in content.splitlines():
                if one_line_flag:
                    one_line_flag = False
                    continue
                details = line.split(' ')
                print(details)
                
                # 室号
                for i in range(3, len(details)):
                    data = (community_name, building_name, details[0], details[1], details[2], details[i])
                    with connection.cursor() as cursor:
                        cursor.execute(sql, data)
                        connection.commit()

# if __name__ == '__main__':
#     connection = connect_db()

#     for community_name in os.listdir(community_name_path):
#         print(community_name)
#         building_name_path = os.path.join(community_name_path, community_name)
        
#         # commnuity_sql
#         data = (community_name)
#         with connection.cursor() as cursor:
#             cursor.execute(commnuity_sql, data)
#             connection.commit()
        
#         for building_name in os.listdir(building_name_path):
#             print(building_name)
#             room_name_path = os.path.join(building_name_path, building_name)
            
#             # building_sql
#             data = ()
#             with connection.cursor() as cursor:
#                 cursor.execute(building_sql, data)
#                 connection.commit()
            
#             print(room_name_path)
#             with open(room_name_path, 'r', encoding='utf-8') as f:
#                 content = f.read()

#             # print(content)
#             for line in content.splitlines():
#                 # print(line)
#                 print('---')
#                 details = line.split(' ')
#                 print(details)
                
#                 # room_sql
#                 data = ()
#                 with connection.cursor() as cursor:
#                     cursor.execute(room_sql, data)
#                     connection.commit()
                
#             break
#         break