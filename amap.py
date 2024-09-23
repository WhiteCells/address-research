import json

import requests

"""
@auther: gql

高德api接口
"""

class AmapApi:
    def __init__(self):
        self.AMAP_KEY = "a5d9c797e4599abbbacc692fd9abac50"

    def amap_api_geo(self, address, city):
        """
        高德api地理解析
        :param address:
        :param city:
        :return:
        """
        url = f"https://restapi.amap.com/v3/geocode/geo?address={address}&key={self.AMAP_KEY}&city={city}"
        response = requests.request("GET", url)

        print(response.text)

    # TODO
    # 把有数据结果的入表，包括level、location 等信息，

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
    {
        "status": "1",
        "info": "OK",
        "infocode": "10000",
        "count": "1",
        "geocodes": [
            {
                "formatted_address": "湖北省黄冈市麻城市富家岗",
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
                "location": "115.012164,31.017582",
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
        url = f"https://restapi.amap.com/v3/geocode/regeo?key={self.AMAP_KEY}&location={location}&poitype={poi_type}&" \
              f"radius={radius}&extensions={extensions}&roadlevel={road_level}"
        response = requests.request("GET", url)

        json_str = response.text
        data = json.loads(json_str)

        # 读取township的值
        township = data['regeocode']['addressComponent']['township']

        return township
