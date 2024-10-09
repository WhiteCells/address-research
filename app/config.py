from pathlib import Path

class MapConfig:
    DIR_PATH = Path('.') / 'map'
    

class OcrConfig:
    INPUT_PATH = MapConfig.DIR_PATH # + <rank>
    OUTPUT_PATH = './res/ocr/res/' # + <filename>


class UnrepeatedConfig:
    INPUT_PATH = OcrConfig.OUTPUT_PATH # 需要去重的地址目录
    OUTPUT_PATH = './res/unrepeated/res/' # + <filename> 去重后的地址保存目录


class AMapApiConfig:
    KEY = 'a5d9c797e4599abbbacc692fd9abac50'
    GEO_URL = 'https://restapi.amap.com/v3/geocode/geo?'
    REGEO_URL = 'https://restapi.amap.com/v3/geocode/regeo?'
    INPUT_PATH = UnrepeatedConfig.INPUT_PATH # + <filename> 待验证地址
    OUTPUT_PATH = './res/amap/res/'


class DBConfig:
    DB_NAME = 'jx_ocr'
    # HOST = '192.168.10.59',
    # 'user': 'research',
    # 'password': '6usKz1Pi8aQ7q8WL',
    # 'database': 'address-research-mater',
    # 'charset': 'utf8mb4',
    # 'cursorclass': pymysql.cursors.DictCursor
