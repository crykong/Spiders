import requests
import json
import time
import random

url = "https://sportapi.fastball2.com/v1/match/getList"


def get_json(current_value):
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
        "current": current_value,
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
        print(res.status_code)
        data_dict = json.loads(res.text)
    return data_dict


def del_data(data_dict):
    file_path = "dic.txt"

    with open("Content", "w", encoding="utf-8") as file:
        for record in data_dict["data"]["records"]:
            for market in record["mg"]:
                mty = market["mty"]
                pe = market["pe"]
                mks = market["mks"]
                nm = market["nm"]
                if nm == "让球":
                    for mk in mks:
                        op = mk["op"]
                        for o in op:
                            na = o["na"]
                            nm = o["nm"]
                            bod = o["bod"]
                            li = o["li"]
                            msg = f"队伍名称 {na} 让球左 {nm} 让球右边 {bod} 确认 {li}\n"
                            file.write(msg)
                        # print(msg)


def wait_time():
    time.sleep(random.random() + random.randint(1, 5))


def main():
    current_page = 1
    for _ in range(current_page):
        print(f'当前页数',current_page)
        data = get_json(current_page)

        if data["success"]:          # Check if success is True
            current_value = data["data"]["current"]  # 当前页
            size_value = data["data"]["size"]  # 大小
            total_value = data["data"]["total"]  #
            pageTotal = data["data"]["pageTotal"]  #

            print(f'Current: {current_value}, Size: {size_value}, Total: {total_value}, PageTotal: {pageTotal}')
            # 计算总页数
            current_page = (total_value + size_value - 1) // size_value
        data = del_data(data)
        datalist = []
    try:
        print('执行条件1')
        print(data)
        for j in range(len(data)):
            print('执行条件2')
            datalist.append(data[j])
        time.sleep(random.randrange(3, 7, 1))
        print("保存数据")
    except Exception as e:
        print(f"发生未知异常: {e}")
if __name__ == '__main__':
    start_time = time.time()
    main()
    print("本次运行时间：{:.6f}".format(time.time() - start_time))