import requests

key = 'a5d9c797e4599abbbacc692fd9abac50'
url = "https://restapi.amap.com/v3/geocode/geo"
file = 'unique_jx_ocr.txt'
out_file = 'belong_jx5.txt'

# 文件的行数
file_line_count = 0
# 成功匹配的行数
matched_line_count = 0

def is_location_in_city(address, target_city):
    global matched_line_count
    # 构建请求参数
    params = {
        'key': key,
        'address': address,
        'city':420115
    }
    response = requests.get(url, params=params)
    
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
    # print(district)
    # print(geocode)
    # 检查返回的城市信息是否包含目标城市
    # if district == target_city:
    #     print(f"{address} 属于 {target_city}")
    #     with open(out_file, 'a', encoding="utf-8") as f:
    #         f.write('address:' + str(params['address']) +
    #                 ',province:' + str(geocode['province']) +
    #                 ',city:'+ str(geocode['city']) +
    #                 ',district:'+ str(geocode['district']) +
    #                 ',level:'+ str(geocode['level']) +
    #                 ',location:' + str(geocode['location']) + '\n')
    #     matched_line_count +=  1
    #     return True

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


with open(file, 'r', encoding='utf-8') as f:
    for line in f:
        file_line_count += 1
        parts = line.split(',', 1)
        text = parts[0].split(':', 1)[1].strip()
        is_location_in_city(text, "江夏区")