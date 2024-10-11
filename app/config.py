# ocr 模块中记录的需要逃过的地址行号
repeated_lines = set()


class MapConfig:
    DIR_PATH = './map'
    

class OcrConfig:
    INPUT_PATH = MapConfig.DIR_PATH
    OUTPUT_PATH = './res/ocr'


class UnrepeatedConfig:
    INPUT_PATH = OcrConfig.OUTPUT_PATH
    OUTPUT_PATH = './res/unrepeated'


class AMapApiConfig:
    KEY = 'a5d9c797e4599abbbacc692fd9abac50'
    GEO_URL = 'https://restapi.amap.com/v3/geocode/geo?'
    REGEO_URL = 'https://restapi.amap.com/v3/geocode/regeo?'
    INPUT_PATH = UnrepeatedConfig.INPUT_PATH
    OUTPUT_PATH = './res/amap'


class DBConfig:
    INPUT_PATH = AMapApiConfig.OUTPUT_PATH
    DATATABLE = 'geocode_huanggang_'
    # sql = f"""
    # INSERT INTO `{DATABASE}`
    # (address, ocr_address, province, city, district, level, location, township)
    # VALUES (%s, %s, %s, %s, %s, %s, %s ,%s);
    # """

    HOST = 'localhost'
    USER = 'root'
    PASSWORD = '123456'
    DATABASE = 'text'

    # HOST = '192.168.10.59',
    # 'user': 'research',
    # 'password': '6usKz1Pi8aQ7q8WL',
    # 'database': 'address-research-mater',
    # 'charset': 'utf8mb4',
    # 'cursorclass': pymysql.cursors.DictCursor

