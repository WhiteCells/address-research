import requests


key = 'a5d9c797e4599abbbacc692fd9abac50'
url = "https://restapi.amap.com/v3/geocode/geo"
city_code = 420115

def is_location_in_city(address, target_city):
    params = {
        'key': key,
        'address': address,
        'city': city_code
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
    formatted_address = geocode['formatted_address']
    print(district)
    print(geocode)
    print(formatted_address)
    
    if district == target_city:
        print(f"{address} 属于 {target_city}")
        with open('singal.txt', 'a', encoding="utf-8") as f:
            f.write('formatted_address:' + str(geocode['formatted_address']) +
                    ',province:' + str(geocode['province']) +
                    ',city:'+ str(geocode['city']) +
                    ',district:'+ str(geocode['district']) +
                    ',level:'+ str(geocode['level']) +
                    ',location:' + str(geocode['location']) + '\n')
        return True

    return False

src_address = input('输入源地址: ')
dest_address = input('输入目标地址: ')

is_location_in_city(src_address, dest_address)