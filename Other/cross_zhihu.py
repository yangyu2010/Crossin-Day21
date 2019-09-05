# -*- coding: utf-8 -*-

'''
@Author: YangYu
@Github: https://github.com/yangyu2010
@Date: 2019-09-03 17:25:18
@LastEditors: YangYu
@LastEditTime: 2019-09-04 15:05:13
'''
'''
爬取某个知乎专栏
'''

import requests
from requests import RequestException
from bs4 import BeautifulSoup
import pdfkit
import os
import lxml
import re
import time

CURRENT_FILE_PATH = os.path.dirname(os.path.abspath('__file__'))
# HTML_FILE_PATH = CURRENT_FILE_PATH + '/' + 'htmls'

url = 'https://zhuanlan.zhihu.com/api/columns/crossin/articles?include=data%5B*%5D.admin_closed_comment%2Ccomment_count%2Csuggest_edit%2Cis_title_image_full_screen%2Ccan_comment%2Cupvoted_followees%2Ccan_open_tipjar%2Ccan_tip%2Cvoteup_count%2Cvoting%2Ctopics%2Creview_info%2Cauthor.is_following%2Cis_labeled%2Clabel_info'
cookie = '_zap=06a20c28-5513-40f3-9d61-7c801cbf9b00; d_c0="AACnOPv2TA-PTpK7WdS6poIAn--DV1oxMcU=|1555643056"; _xsrf=wIEd6tN4RmC6MdK6buaARNa9osBmZhGP; capsion_ticket="2|1:0|10:1567129324|14:capsion_ticket|44:OTJkZWUyN2JhZTA1NGI4Mjk0NzZmYTJlNGY0OTM0Yzk=|b6a49ecdcb4bc80b7c0040ee14ef33c4ae3b4f4a0696cdfc9feb7606234dff1b"; z_c0="2|1:0|10:1567129348|4:z_c0|92:Mi4xRkh4MUFBQUFBQUFBQUtjNC1fWk1EeWNBQUFDRUFsVk5CQXlRWFFEeDRYT3JoUzFsa19VZ1J4R0FtYUlaRGUyRldR|034dbd023e3215ef217d74f0586fa372f59c1b59887c78ebd0a9d69a3c96a1a8"; tshl=; q_c1=19f51643b9714cdb9ccee998f8f14de4|1567130281000|1567130281000; tst=r; tgw_l7_route=66cb16bc7f45da64562a077714739c11'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
headers = {'cookie': cookie, 'user-agent': user_agent}


'''
循环遍历
'''
def get_zhihu_data() -> list:
    array_list = []
    global url
    
    while True:
        try:
            resp = requests.get(url, headers=headers)
        except RequestException as error:
            print('get data error', error)
        else:
            if resp.status_code != 200:
                print('get data status_code error')
                break
            j = resp.json()
            data = j['data']
            for article in data:
                print(article.get('id'), article.get('title')) 
                info = {
                    'id': article.get('id'), 
                    'title': article.get('title'),
                }
                array_list.append(info)
            
            paging = j.get('paging')
            if paging['is_end']:
                break
            url = paging['next']
            url = url.replace('zhuanlan.zhihu.com', 'zhuanlan.zhihu.com/api')
        time.sleep(2)

        # 我只抓取第一页数据, 如要抓取所有, 注释掉break
        break
    return array_list


def save_data_html(array_list):
    index = 1
    for item in array_list:
        url = 'https://zhuanlan.zhihu.com/p/%s' % item['id']
        name = f'{index:03}' + '-' + item['title']
        while '/' in name:
            name = name.replace('/', '')
        html = requests.get(url, headers=headers).text

        soup = BeautifulSoup(html, 'lxml')
        content = soup.prettify()
        # content = soup.find(class_='Post-Main Post-NormalMain').prettify()
        content = content.replace('data-actual', '')
        content = content.replace('h1>', 'h2>')
        content = re.sub(r'<noscript>.*?</noscript>', '', content)
        content = re.sub(r'src="data:image.*?"', '', content)
        # content = '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><h1>%s</h1>%s</body></html>' % (name, content)

        with open('%s.html' % name, 'w') as f:
            f.write(content)
        index += 1


def cover_html_to_pdf():
    file_list =  os.listdir(CURRENT_FILE_PATH)
    all_html_list = []
    for path in file_list:
        file_extension = os.path.splitext(path)[1]
        if file_extension == '.html':
            all_html_list.append(path)
    all_html_list.sort()
    print(all_html_list)

    pdfkit.from_file(all_html_list, 'cross_zhihu.pdf')
    

    
# l = get_zhihu_data()
# save_data_html(l)
# cover_html_to_pdf()
