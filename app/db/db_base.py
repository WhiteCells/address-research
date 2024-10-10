import sys

import pymysql

from amap import AmapApi

"""
@auther: gql

根据查询到数据的地址补充镇一级的数据
"""

amap_api = AmapApi()

# 数据库连接配置
db_config = {
    'host': '192.168.10.59',  # 例如：'localhost'
    'user': 'research',  # 您的数据库用户名
    'password': '6usKz1Pi8aQ7q8WL',  # 您的数据库密码
    'database': 'address-research-mater',  # 您的数据库名
    'charset': 'utf8mb4',  # 字符编码
    'cursorclass': pymysql.cursors.DictCursor  # 使用字典游标
}

"""
SELECT * FROM `address-research-mater`.`addresses`;
"""

"""
UPDATE `address-research-mater`.`addresses` SET `township` = NULL WHERE `id` = 1;
"""


def se_db(table):
    # 连接到数据库
    try:
        connection = pymysql.connect(**db_config)
        print("成功连接到数据库")

        # 创建一个cursor对象
        with connection.cursor() as cursor:
            # 编写SQL查询语句
            sql = f"SELECT * FROM `address-research-mater`.`{table}` WHERE `township` IS NULL"

            # 执行SQL语句
            cursor.execute(sql)

            # 获取所有查询结果
            results = cursor.fetchall()

            # 打印结果
            for row in results:
                print(row)  # 如果你设置了cursorclass为DictCursor，这里可以直接用print(row['id'], row['name'])来访问字段

                township = amap_api.amap_api_re_geo(row['location'])
                print(township)
                if township != "":
                    update_db(table, township, row['id'])


    except pymysql.MySQLError as e:
        print(f"数据库错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        # 关闭数据库连接
        if connection:
            connection.close()
            print("数据库连接已关闭")


def update_db(table, township, id_):
    # 连接到数据库
    try:
        connection = pymysql.connect(**db_config)
        print("成功连接到数据库")

        # 创建一个cursor对象
        with connection.cursor() as cursor:
            # 编写SQL更新语句
            # 注意：使用参数化查询来防止SQL注入
            sql = f"UPDATE `address-research-mater`.`{table}` SET `township` = %s WHERE `id` = %s;"

            # 执行SQL语句
            cursor.execute(sql, (township, id_))

            # 提交事务
            connection.commit()

            print(f"成功更新了ID为{id_}的记录")

    except pymysql.MySQLError as e:
        print(f"数据库错误: {e}")
        # 如果发生错误，可以选择回滚
        if connection:
            connection.rollback()
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        # 关闭数据库连接
        if connection:
            connection.close()
            print("数据库连接已关闭")


table_name = "hg_amap_address"
se_db(table_name)

# township = amap_api.amap_api_re_geo('114.754592,31.022195')
# print(township)