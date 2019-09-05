# -*- coding: utf-8 -*-

'''
@Author: YangYu
@Github: https://github.com/yangyu2010
@Date: 2019-09-04 15:32:37
@LastEditors: YangYu
@LastEditTime: 2019-09-05 15:42:49
@Desc: 链接租房信息爬取
'''

from bs4 import BeautifulSoup
import requests
import os
import csv

CURRENT_FILE_PATH = os.path.abspath(os.path.dirname(__file__))
CSV_FILE_PATH = CURRENT_FILE_PATH + '/' + 'zufang_wuhan.csv'

url = 'https://wh.lianjia.com/zufang/'
cookie = 'lianjia_uuid=a3d1bc1a-9084-4d9a-a19e-ee776e98b57e; all-lj=8e5e63e6fe0f3d027511a4242126e9cc; lianjia_ssid=101c5e35-237e-4b12-b271-69521156e76f; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiNGZiNDJhNWY3MjE2MGEwNGUwYWQ4ZDMxODBiMTVlYmE3NjY2MDEzYzM1OGRhZjFkNDFjYjk3M2FmN2YxOTE4M2ZhYmVhY2IzZDk1ZDRkZWFjNGIzMjVmY2M1NzkxNmZhNjk1NTg2MDU4NjViYjNmNmM2N2MwODZhNWJhZjRkZDBiYzNmZmQ2OTlkOWJlODI1ZGE0MzU4OWNkZWRmYTA2YmQ3OTlkYWU1ZTc2MDk4MjM0OWExMWE5NzU2OGZmMjZjODFlM2RjMWFjYWZhMTAwNTNkYTBmNDMzYTliM2QyMGZhMGMxMTc5NTZkMWQ3YmFiZGJiMjU3YTQ5MTZlYTFkZTc3MjZjOWVjZWI0OTRhZTVlZWQ0OTg1YWZjZTFjN2U0ZWQ0MzhiZmU0OTU3ZGM3NDA2NzA4ZmU0ZGRjOWZmMjQ4Y2VmZDZmZjY5NWQ2MmZmYjdjNTliMzE1OWQ3OGIzZlwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJiMzI4NWQ5NlwifSIsInIiOiJodHRwczovL3doLmxpYW5qaWEuY29tL3p1ZmFuZyIsIm9zIjoid2ViIiwidiI6IjAuMSJ9'
user_Agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
headers = {'cookie': cookie, 'User-Agent': user_Agent}


# csv文件先写入默认行 用w覆盖
def config_default_csv():
    with open(CSV_FILE_PATH, "w", encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['标题', "链接", '详细地址', "房屋面积", '朝向', '房屋格式', '楼层', '价格'])
config_default_csv()


# 将数据写入csv
def save_data_to_csv(info: []):
    with open(CSV_FILE_PATH, "a+", encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(info)
        
# 获取数据
def get_lianjia_data(url, headers):
    try:
        resp = requests.get(url, headers=headers)
    except:
        print('get data error')
        return None
    else:
        text = resp.text
        soup = BeautifulSoup(text, 'html.parser')
        content_list = soup.find_all('div', {'class': 'content__list--item'})

        item_info_list = []
        for item in content_list:
            item_info = []
            p1 = item.find('p', {'class': 'content__list--item--title twoline'})
            title = p1.find('a').get_text()
            url = p1.find('a').get('href')
            item_info.append(title)
            item_info.append(url)

            p2 = item.find('p', {'class': 'content__list--item--des'})
            text_list = p2.text.split()
            address = text_list.pop(0)
            space = text_list[1]
            direction = text_list[2][1:]
            structure = text_list[4]
            level = text_list[6] + text_list[7]
            # print(address, space, direction, structure, level)
            item_info.append(address)
            item_info.append(space)
            item_info.append(direction)
            item_info.append(structure)
            item_info.append(level)

            span = item.find('span', {'class': 'content__list--item-price'})
            print(span)
            price = span.get_text()
            item_info.append(price)

            item_info_list.append(item_info)
        return item_info_list


def run():
    config_default_csv()
    item_info_list = get_lianjia_data(url, headers)
    for item in item_info_list:
        save_data_to_csv(item)


run()