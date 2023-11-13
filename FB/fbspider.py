import requests
import json
import time
import random

url = "https://sportapi.fastball2.com/v1/match/getList"


def get_json(page):
    HEADERS_1 = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Host": "sportapi.fastball2.com",
        "Origin": "https://test.f66b88sport.com",
        "Referer": "https://test.f66b88sport.com/",
        "Sec-Ch-Ua": '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    }

    # DataJson
    payload = {
        "languageType": "CMN",
        "current": page,
        "orderBy": "1",
        "isPC": "true",
        "sportId": "1",
        "type": "3",
    }
    # {"languageType":"CMN","current":1,"orderBy":1,"isPC":true,"sportId":1,"type":3}   #第一页
    # {"languageType":"CMN","current":2,"orderBy":1,"isPC":true,"sportId":1,"type":3}   #第二页
    #
    print(payload)
    res = requests.post(url=url, headers=HEADERS_1, json=payload)
    # 检查  status code 200
    if res.status_code == 200:
        data_dict = json.loads(res.text)
        return data_dict


def get_data(json):
    data, _, page = del_data(json)
    sava_data(data)
    if page > 1:
        while True:
            time.sleep(random.random() + random.randrange(2, 4, 1))
            json = get_json(page)
            data, current_value, page = del_data(json)
            sava_data(data)
            if current_value == page:
                break


def deal_data(data):
    # if isinstance(data, str):  # 如果是字符串，认为是 JSON 字符串
    # data = json.loads(data)
    items = []
    records_result = data['data']['records']
    for i in records_result:
        cache = []
        companyind_text = i['mg']

        for market in companyind_text:
            mks = market.get("mks", [])
            for mk in mks:
                ops = mk.get("op", [])
                for op in ops:
                    cache.append(op)

        items.append({"data": cache})

    pages = data['pageTotal']
    return items


def sava_data(data):
    with open("save.txt", "a", encoding="utf-8") as file:
        json_data = json.dumps(data, ensure_ascii=False)
        file.write(json_data + "\n")
    print("保存成功")

def del_data(data_dict):
    current_value = data_dict["data"]["current"]  # 当前页
    # size_value = data_dict["data"]["size"]  # 大小
    total_value = data_dict["data"]["total"]  #
    # pageTotal = data_dict["data"]["pageTotal"]  #
    pages = total_value // 50 + 1 if total_value % 50 != 0 else total_value // 50
    items = []
    for record in data_dict["data"]["records"]:
        for market in record["mg"]:
            mty = market["mty"]
            pe = market["pe"]
            mks = market["mks"]
            nm = market["nm"]
            if nm == "让球":  # 后续在加条件判断
                for mk in mks:
                    op = mk["op"]
                    for o in op:
                        cache = []
                        # na = o["na"]
                        # nm = o["nm"]
                        # bod = o["bod"]
                        # li = o["li"]
                        # msg = f"队伍名称 {na} 让球左 {nm} 让球右边 {bod} 确认 {li}\n"
                        # file.write(msg)
                        cache.append(op)
                    items.append({"data": cache})
        return items, int(current_value), int(pages)


def wait_time():
    time.sleep(random.random() + random.randint(1, 5))


def main():
    print('首次运行请在代码中修改MySQL数据库密码和数据库名称')
    page = int(input('请输入获取页数：'))
    json = get_json(1)
    get_data(json)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("本次运行时间：{:.6f}".format(time.time() - start_time))
