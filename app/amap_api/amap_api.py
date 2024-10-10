import requests
import os
import json
import pandas as pd
from app.config import AMapApiConfig


def amap_api_re_geo(self, location, poi_type="", radius=1000, extensions='all', road_level=0):
    """
    高德api地理逆解析
    :param location:
    :param poi_type:
    :param radius:
    :param extensions:
    :param road_level:
    :return:
    """
    url = f"https://restapi.amap.com/v3/geocode/regeo?"\
            f"key={self.AMAP_KEY}&location={location}&poitype={poi_type}&" \
            f"radius={radius}&extensions={extensions}&roadlevel={road_level}"
    response = requests.request("GET", url)

    json_str = response.text
    data = json.loads(json_str)

    # 读取township的值
    township = data['regeocode']['addressComponent']['township']

    return township


def process_one_line(ocr_address, target_district, adcode):
    """
    处理单行地址，判断地址是否在地级市
    :ocr_address: ocr 识别的地址
    :target_district: 实际地级市
    :adcode: citycode
    :return: 返回匹配的地址
    """
    print('=> address: ', ocr_address)
    print('=> target_district: ', target_district)
    print('=> adcode: ', adcode)
    
    params = {
        'key': AMapApiConfig.KEY,
        'address': ocr_address,
        'city': adcode
    }
    response = requests.get(AMapApiConfig.GEO_URL, params=params)
    
    if response.status_code != 200:
        print(f"请求失败: HTTP状态码 {response.status_code}")
        return None

    result = response.json()

    if result['status'] == '0':
        print(result['info'])
        return None
    
    if result['count'] == '0':
        print(f"{ocr_address} 不属于 {target_district}")
        return None
    
    geocode = result['geocodes'][0]
    district = geocode['district']

    if district == target_district:
        print(f"=> {ocr_address} 属于 {target_district}")
        return 'formatted_address:' + str(geocode['formatted_address']) + \
               ',ocr_address:' + str(params['address']) + \
               ',province:' + str(geocode['province']) + \
               ',city:'+ str(geocode['city']) + \
               ',district:'+ str(geocode['district']) + \
               ',level:'+ str(geocode['level']) + \
               ',location:' + str(geocode['location'])

    return None


def process_res_unrepeated_dir():
    """
    验证指定目录下的去重地址
    """
    for root, dirs, files in os.walk(AMapApiConfig.INPUT_PATH):
        for file in files:
            if not file.endswith(".txt"):
                continue
            
            file_path = os.path.join(root, file)
            print('=> processing: ', file_path)
            
            # 取出文件名（不包含后缀）
            filename = os.path.basename(file_path).split('.')[0]
            
            # 取出地图等级
            rank = filename.split('_')[-1]
            
            # 取出地级市
            target_district = filename.split('_')[-2]
            
            # 从 citycode.xlsx 中查找 target_district 对应的 adcode
            df = pd.read_excel('./app/amap_api/citycode.xlsx')
            adcode = df.loc[df['中文名'] == '江夏区', 'adcode'].values[0]
            
            # 确保 res/amap 目录存在
            if not os.path.exists(AMapApiConfig.OUTPUT_PATH):
                os.mkdir(AMapApiConfig.OUTPUT_PATH)
            
            # 确保 res/amap/<rank> 目录存在
            if not os.path.exists(f'{AMapApiConfig.OUTPUT_PATH}/{rank}'):
                os.mkdir(f'{AMapApiConfig.OUTPUT_PATH}/{rank}')
            
            # 逐行检查文件中地址是否在属于 target_district
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    ocr_address = line.split(',', 1)[0].split(':', 1)[1].strip()
                    res = process_one_line(ocr_address, target_district, adcode)
                    if not res:
                        continue
                    
                    with open(f'{AMapApiConfig.OUTPUT_PATH}/{rank}/{filename}.txt', 'a', encoding='utf-8') as f:
                        f.write(res)