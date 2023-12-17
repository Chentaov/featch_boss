import json

jobType = 1901 #全职 1903=兼职
experience = 102 #经验要求102=应届，103=一年以内，101=不限
degree=204 #学历204=硕士，203=本科
scale=303 #公司规模303=100-499人，304=500-999人，305=1000-9999人

endPage_notice = '没有找到相关职位'

def get_city_code(city_name:str): #获取城市代码
    city_code = {}
    with open("data_store/city.json", "r", encoding="utf-8") as f:
        content = json.load(f)
        city = content['zpData']['cityList']  #城市具体信息列表
        for item in city:
            for p in item['subLevelModelList']:
                city_code[p['name']] = p['code']
    # print(city_code)
    return str(city_code.get(city_name))

def get_region_code(region:str): #获取区代码
    region_code = {}
    with open("data_store/city.json", "r", encoding="utf-8") as f:
        content = json.load(f)
        city = content['zpData']['cityList']  #城市具体信息列表
        for item in city:
            for c in item['subLevelModelList']:
                try:
                    for r in c['subLevelModelList']:
                        region_code[r['name']] = r['code']
                except TypeError:
                    continue
    return str(region_code.get(region))
# print(get_region_code('苏州工业园区'))
# print(get_province_code('苏州'))