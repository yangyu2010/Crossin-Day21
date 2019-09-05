# -*- coding: utf-8 -*-

'''
@Author: YangYu
@Github: https://github.com/yangyu2010
@Date: 2019-09-05 17:42:49
@LastEditors: YangYu
@LastEditTime: 2019-09-05 19:58:01
@Desc: 智联招聘搜索爬取(搜索python)
'''

import requests
from http import HTTPStatus
from bs4 import BeautifulSoup
import os
import csv
import time
from lxml import html


CURRENT_FILE_PATH = os.path.abspath(os.path.dirname(__file__))
CSV_FILE_PATH = CURRENT_FILE_PATH + '/' + 'zhilian.csv'


url = 'https://fe-api.zhaopin.com/c/i/sou'
cookie = 'LastCity=%E6%AD%A6%E6%B1%89; LastCity%5Fid=736; ZL_REPORT_GLOBAL={%22//www%22:{%22seid%22:%22%22%2C%22actionid%22:%22f9fca19a-ff96-4114-8e1f-c6dea578ba5e-cityPage%22}%2C%22sou%22:{%22actionid%22:%22e4e1cd95-5b17-40b4-89fd-501848a4944b-sou%22%2C%22funczone%22:%22smart_matching%22}%2C%22jobs%22:{%22recommandActionidShare%22:%22d3ca57e5-6674-47c4-b905-f97259d40e49-job%22%2C%22funczoneShare%22:%22dtl_best_for_you%22}}; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1567682047; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1567669661; ZP_OLD_FLAG=false; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216d0064aae32ff-081989b9d544a7-3f616f4a-2359296-16d0064aae49ee%22%2C%22%24device_id%22%3A%2216d0064aae32ff-081989b9d544a7-3f616f4a-2359296-16d0064aae49ee%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; sts_evtseq=8; sts_sid=16d0120abeb1e1-0d89eef402d8fd8-3f616f4a-2359296-16d0120abec30d; __utma=269921210.413074937.1567669681.1567669681.1567669681.1; __utmc=269921210; __utmz=269921210.1567669681.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); dywea=95841923.2855027131560349700.1567669660.1567669660.1567669660.1; dywec=95841923; CANCELALL=0; POSSPORTLOGIN=5; sou_experiment=psapi; zp_src_url=https%3A%2F%2Fwww.zhaopin.com%2F; ZPCITIESCLICKED=|736; dywez=95841923.1567669660.1.1.dywecsr=(direct)|dyweccn=(direct)|dywecmd=(none)|dywectr=undefined; jobRiskWarning=true; sajssdk_2015_cross_new_user=1; sts_chnlsid=Unknown; sts_deviceid=16d0064aaced23-0c82ac28319dbd-3f616f4a-2359296-16d0064aacfcd1; sts_sg=1; acw_tc=2760828c15676696601857330e3d1f02b27f53d79600b4203a3dd447103a95; adfbid=0; adfbid2=0; adfcid=none; adfcid2=none; urlfrom=121126445; urlfrom2=121126445; x-zp-client-id=efccda10-3f3b-474f-b676-5dc5c0730488'
cookie_desc = 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216d0064aae32ff-081989b9d544a7-3f616f4a-2359296-16d0064aae49ee%22%2C%22%24device_id%22%3A%2216d0064aae32ff-081989b9d544a7-3f616f4a-2359296-16d0064aae49ee%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; LastCity=%E6%AD%A6%E6%B1%89; LastCity%5Fid=736; ZL_REPORT_GLOBAL={%22//www%22:{%22seid%22:%22%22%2C%22actionid%22:%22f9fca19a-ff96-4114-8e1f-c6dea578ba5e-cityPage%22}%2C%22sou%22:{%22actionid%22:%22f1e980f5-c987-45eb-914e-17736d2bf7bf-sou%22%2C%22funczone%22:%22smart_matching%22}%2C%22jobs%22:{%22recommandActionidShare%22:%22ba64a02e-7bcf-4071-a3af-72d06e278d1d-job%22%2C%22funczoneShare%22:%22dtl_best_for_you%22}}; sts_evtseq=14; sts_sid=16d0120abeb1e1-0d89eef402d8fd8-3f616f4a-2359296-16d0120abec30d; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1567682682; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1567669661; ZP_OLD_FLAG=false; __utma=269921210.413074937.1567669681.1567669681.1567669681.1; __utmc=269921210; __utmz=269921210.1567669681.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); dywea=95841923.2855027131560349700.1567669660.1567669660.1567669660.1; dywec=95841923; CANCELALL=0; POSSPORTLOGIN=5; sou_experiment=psapi; zp_src_url=https%3A%2F%2Fwww.zhaopin.com%2F; ZPCITIESCLICKED=|736; dywez=95841923.1567669660.1.1.dywecsr=(direct)|dyweccn=(direct)|dywecmd=(none)|dywectr=undefined; jobRiskWarning=true; sajssdk_2015_cross_new_user=1; sts_chnlsid=Unknown; sts_deviceid=16d0064aaced23-0c82ac28319dbd-3f616f4a-2359296-16d0064aacfcd1; sts_sg=1; acw_tc=2760828c15676696601857330e3d1f02b27f53d79600b4203a3dd447103a95; adfbid=0; adfbid2=0; adfcid=none; adfcid2=none; urlfrom=121126445; urlfrom2=121126445; x-zp-client-id=efccda10-3f3b-474f-b676-5dc5c0730488'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Safari/605.1.15'
headers = {'cookie': cookie, 'user-agent': user_agent}
headers_desc = {'cookie': cookie_desc, 'user-agent': user_agent}
params = {
    'pageSize':90,
    'cityId':736,
    'workExperience':-1,
    'education':-1,
    'companyType':-1,
    'employmentType':-1,
    'jobWelfareTag':-1,
    'kt':3,
    '_v':0.08497719,
    'x-zp-page-request-id':'c4694c82889b4f69b88a9f8ec9eb0b4b-1567671551502-254252',
    'x-zp-client-id':'efccda10-3f3b-474f-b676-5dc5c0730488',
}


class ZhiLianZhaoPin:

    def __init__(self):
        self.config_default_csv()

    # csv文件先写入默认行 用w覆盖
    def config_default_csv(self):
        with open(CSV_FILE_PATH, "w", encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['标题', "链接", '详细地址', "房屋面积", '朝向', '房屋格式', '楼层', '价格'])
            # ["职位", "工作地点", "公司", "规模", "工作性质", "公司类型", "工作类型", "薪酬", "福利", "工作经验", "职位详细描述"]

    # 将数据写入csv
    def save_data_to_csv(self, info: []):
        with open(CSV_FILE_PATH, "a+", encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(info)

    # 根据关键字来获取职位信息
    def request_job_info(self, keyword: str):
        new_params = params
        if keyword:
            new_params['kw'] = keyword
        else:
            new_params['kw'] = 'iOS'
        resp = requests.get(url, params=new_params, headers=headers)
        assert resp.status_code == HTTPStatus.OK
        return resp.json()

    # 读取数据
    def read_jobs_from_data(self, data):
        assert data.get('code') == HTTPStatus.OK
        print(data)
        results_list = data.get('data').get('results')
        jobs_info_list = []
        for item in results_list:
            jobName = item.get('jobName')
            company_name = item.get('company').get('name')
            city = item.get('city').get('display')
            business_area = item.get('businessArea')
            eduLevel = item.get('eduLevel').get('name')
            url = item.get('positionURL')
            workingExp = ''
            if item.get('workingExp'):
                workingExp = item.get('workingExp').get('name')
            desc = self.read_job_desc(url)
            job_info = [jobName, company_name, city, business_area, eduLevel, workingExp, url, desc]
            jobs_info_list.append(job_info)
            # 过3s处理下一个
            time.sleep(3)
        return jobs_info_list

    # 读取职位详细信息
    def read_job_desc(self, job_desc_url):
        resp = requests.get(job_desc_url, headers=headers_desc)
        assert resp.status_code == HTTPStatus.OK
        html = resp.text
        print(html)
        soup = BeautifulSoup(html, 'html.parser')
        describtion__detail = soup.find('div', {'class': 'describtion__detail-content'})
        if describtion__detail is None:
            print('读取职位详细信息失败')
            return ''
        describtion__detail_list = describtion__detail.find_all('p')
        desc = ''
        for item in describtion__detail_list:
            desc += item.get_text()
            desc += '\n'
        return desc

    def run(self):
        # keywords = input("请输入你要查询的关键字：")
        keywords='ios'
        if keywords:
            data = self.request_job_info(keywords)
            data_list = self.read_jobs_from_data(data)
            # 先输入整个列表
            for info in data_list:
                self.save_data_to_csv(info)
        else:
            print('输入有误')


# z = ZhiLianZhaoPin()
# z.run()
# z.read_job_desc('https://jobs.zhaopin.com/CCL1206970160J00455790201.htm')

# url = 'https://jobs.zhaopin.com/CCL1206970160J00455790201.htm'
# job_web = requests.session()
# headers = {
#     'cookie': 'LastCity=%E6%AD%A6%E6%B1%89; LastCity%5Fid=736; ZL_REPORT_GLOBAL={%22//www%22:{%22seid%22:%22%22%2C%22actionid%22:%2212463738-cbcb-436a-a0f2-eee3a9a3f017-cityPage%22}%2C%22sou%22:{%22actionid%22:%22f04a549d-8d1d-41f0-9dc2-15f4b5c798ec-sou%22%2C%22funczone%22:%22smart_matching%22}%2C%22jobs%22:{%22recommandActionidShare%22:%220913cb69-777b-4d7b-b55d-0742e7e7031d-job%22%2C%22funczoneShare%22:%22dtl_best_for_you%22}}; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216d0064aae32ff-081989b9d544a7-3f616f4a-2359296-16d0064aae49ee%22%2C%22%24device_id%22%3A%2216d0064aae32ff-081989b9d544a7-3f616f4a-2359296-16d0064aae49ee%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24latest_referrer_host%22%3A%22www.google.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; sts_evtseq=34; sts_sid=16d0120abeb1e1-0d89eef402d8fd8-3f616f4a-2359296-16d0120abec30d; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1567683775; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1567669661,1567683756; ZP_OLD_FLAG=false; __utma=269921210.413074937.1567669681.1567683469.1567683756.3; __utmb=269921210.1.10.1567683756; __utmc=269921210; __utmz=269921210.1567683756.3.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); dywea=95841923.2855027131560349700.1567669660.1567669660.1567683469.2; dyweb=95841923.2.10.1567683469; dywec=95841923; adfbid=0; adfbid2=0; adfcid=www.google.com; adfcid2=www.google.com; urlfrom=121114584; urlfrom2=121114584; dywez=95841923.1567683469.2.2.dywecsr=passport.zhaopin.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/additional/bindmobile; CANCELALL=0; POSSPORTLOGIN=5; sou_experiment=psapi; zp_src_url=https%3A%2F%2Fwww.zhaopin.com%2F; ZPCITIESCLICKED=|736; jobRiskWarning=true; sajssdk_2015_cross_new_user=1; sts_chnlsid=Unknown; sts_deviceid=16d0064aaced23-0c82ac28319dbd-3f616f4a-2359296-16d0064aacfcd1; sts_sg=1; acw_tc=2760828c15676696601857330e3d1f02b27f53d79600b4203a3dd447103a95; x-zp-client-id=efccda10-3f3b-474f-b676-5dc5c0730488',
#     "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Safari/605.1.15"
# }
# req = job_web.get("{}".format(url), headers=headers_desc)
# assert req.status_code == HTTPStatus.OK
# tree = html.fromstring(req.text)
# print(req.text)
# info_list = tree.xpath('//div[@class="describtion"]/div/p/span/text()')
# info = ' '.join(info_list)
# print(info)

# resp = requests.get(url, params=params, headers=headers)
# assert resp.status_code == HTTPStatus.OK
# print(resp.json())