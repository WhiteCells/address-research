import requests
def is_location_in_city(address, target_city, key):
    # 地理编码API的URL
    url = "https://restapi.amap.com/v3/geocode/geo"

    # 构建请求参数
    params = {
        'key': key,
        'address': address,
        'city':421181
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:  #响应成功
        result = response.json()
        if result['status'] == '0':    #打印出错误码
           print(result['info'])
        else:                          #为了区分是否是无法找到地址
         if result['status'] == '1' and result['count'] != '0':

            geocode = result['geocodes'][0]
            district = geocode['district']
            print(district)
            print(geocode)
            # 检查返回的城市信息是否包含目标城市
            if district == target_city:
                print(f"{address} 属于 {target_city}")
                with open('demo_geocode2.txt', 'a', encoding="utf-8") as f:
                 f.write('address:' + str(params['address']) +
                         ',province:' + str(geocode['province']) +
                         ',city:'+str(geocode['city'])+
                          ',district:'+str(geocode['district'])+
                          ',level:'+str(geocode['level'])+
                         ',location:' + str(geocode['location']) + '\n')
                return True
            else:
                print(f"{address} 不属于 {target_city}")
                return False
        #if result['status'] == '1' and result['count']=='0':
         else:
            print(f"无法找到地址: {address}")
            return False
    else:
        print(f"请求失败: HTTP状态码 {response.status_code}")
        return False

with open('newdemo_z63(1).txt', 'r', encoding='utf-8') as file:
    for line in file:
        parts = line.split(',', 1)
        text = parts[0].split(':', 1)[1].strip()

        is_location_in_city(text, "麻城市", "a5d9c797e4599abbbacc692fd9abac50")