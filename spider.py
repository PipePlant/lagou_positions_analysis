# coding=utf-8
import requests
import time
import csv

url_start = 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE?oquery=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&fromSearch=true&labelWords=relative'
url_tar = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'

# 模仿浏览器请求
headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
        'Referer': 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=&labelWords=hot', # 从浏览器上拉一个下来
    }
csv_path = './csvs/'
with open(csv_path +'lagou_data.csv','w',encoding='gbk',newline='') as fd:
    csv_write = csv.writer(fd)
    title = ['id','职位','城市','学历','工作年限','薪资','第一标签','第二标签','第三标签','技能库','公司名称','融资阶段','公司规模']
    csv_write.writerow(title)

    # 一个会话中最多包含30页
    for page in range(1,31):
        print('[Page: {}]'.format(page))
        s = requests.session()
        s.get(url_start, headers=headers, timeout=2)  # 请求首页获取cookies
        cookies = s.cookies  # 为此次获取的cookies

        data = {
            'first':'true',
            'kd':'数据分析',
            'pn':page
        }

        response  = s.post(url_tar,headers=headers,cookies=cookies,data=data)
        response.encoding = 'utf-8'

        results = response.json()
        positions = results['content']['positionResult']['result']
        for position in positions:
            p_data = []
            p_data.append(position['positionId'])
            p_data.append(position['positionName'])
            p_data.append(position['city'])
            p_data.append(position['education'])
            p_data.append(position['workYear'])
            p_data.append(position['salary'])
            p_data.append(position['firstType'])
            p_data.append(position['secondType'])
            p_data.append(position['thirdType'])
            p_data.append(str(position['skillLables']))
            p_data.append(position['companyShortName'])
            p_data.append(position['financeStage'])
            p_data.append(position['companySize'])

            csv_write.writerow(p_data)
        time.sleep(5)

print('[---Finish---]')