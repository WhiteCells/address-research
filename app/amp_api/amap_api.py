import json
import requests
from app.config import AMapApiConfig

# 有数据的结果
"""
{
    "status": "1",
    "info": "OK",
    "infocode": "10000",
    "count": "1",
    "geocodes": [
        {
            "formatted_address": "湖北省黄冈市麻城市朱金冲",
            "country": "中国",
            "province": "湖北省",
            "citycode": "0713",
            "city": "黄冈市",
            "district": "麻城市",
            "township": [],
            "neighborhood": {
                "name": [],
                "type": []
            },
            "building": {
                "name": [],
                "type": []
            },
            "adcode": "421181",
            "street": [],
            "number": [],
            "location": "115.153719,31.597735",
            "level": "村庄"
        }
    ]
}
"""
# 没有数据的结果
"""
{
    "status": "0",
    "info": "ENGINE_RESPONSE_DATA_ERROR",
    "infocode": "30001"
}
"""

"""
从不重复的地址中验证地址

"""
class AmapApi:
    def __init__(self):
        self.key = AMapApiConfig.KEY
        self.input_path = AMapApiConfig.INPUT_PATH
        self.output_path = AMapApiConfig.OUTPUT_PATH

    # TODO
    # 把有数据结果的入表，包括level、location 等信息，



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

    def is_location_in_city(self, address, target_city):
        # 构建请求参数
        params = {
            'key': self.AMAP_KEY,
            'address': address,
            'city':420115
        }
        response = requests.get(self.url, params=params)
        
        if response.status_code != 200:
            print(f"请求失败: HTTP状态码 {response.status_code}")
            return False

        result = response.json()

        if result['status'] == '0':
            print(result['info'])
            return False
        
        if result['count'] == '0':
            print(f"{address} 不属于 {target_city}")
            return False
        
        geocode = result['geocodes'][0]
        district = geocode['district']

        if district == target_city:
            print(f"{address} 属于 {target_city}")
            with open(out_file, 'a', encoding="utf-8") as f:
                f.write('formatted_address:' + str(geocode['formatted_address']) +
                        ',ocr_address:' + str(params['address']) +
                        ',province:' + str(geocode['province']) +
                        ',city:'+ str(geocode['city']) +
                        ',district:'+ str(geocode['district']) +
                        ',level:'+ str(geocode['level']) +
                        ',location:' + str(geocode['location']) + '\n')
            return True

        return False