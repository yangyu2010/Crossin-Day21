# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'Cross-Day21/day1'))
	print(os.getcwd())
except:
	pass

#%%
import requests
while True:
    city = input('请输入你想查询的城市:')
    r = requests.get('http://wthrcdn.etouch.cn/weather_mini?city=%s' % city)
    response = r.json()
    code = response.get('status')
    if code == 1000:
        forecast = response['data']['forecast']
        info = forecast[0]
        print('%s, %s, %s, %s, %s' % (info['date'], info['type'], info['fengxiang'], info['high'], info['low']))
    else:
        if code == 1002:
            print('输入城市名有误')
        else:
            print(response.get('desc'), defalut='请求接口失败')


