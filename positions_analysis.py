# coding=utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

csv_path = './csvs/'
image_path = './images/'
file = csv_path+'lagou_data.csv'
# 读取文件
df = pd.read_csv(file,encoding='gbk')

'''城市与职位数量关系'''
plt.figure(dpi=128,figsize=(10, 6))
city_posn_obj = df['城市'].value_counts()
city_posn_obj.plot(kind='bar')
cp_index_data = []
for index in city_posn_obj.index:
    cp_index_data.append(index)
xax_data = range(0,len(cp_index_data))
yax_data = city_posn_obj.values

# 设置表，xy轴名称
plt.title("城市-职位数量",fontsize=20)
plt.xlabel("城市",fontsize=15)
plt.ylabel("职位数量",fontsize=15)
plt.xticks(rotation=360)
# 显示每个柱的数据
for x, y in zip(xax_data,yax_data):
    plt.text(x, y + 0.05, '%s' % y, ha='center', va='bottom')

plt.savefig(image_path+'city_positions.png',bbox_inches='tight')

'''薪资与职位数量关系'''
plt.figure(dpi=128,figsize=(10, 6))
salary_posn_obj = df['薪资'].value_counts()
salary_data = pd.Series([])
for x,y in zip(salary_posn_obj.index,salary_posn_obj.values):
    pattern = re.compile(r'(\d+)k.*?(\d+)k',re.I) # 查找薪资
    result = pattern.search(x)
    salary = int(result.group(1))*800+int(result.group(2))*200 # 粗略的用一个值代替计算薪资区间
    key = None
    if salary < 10000:
        key = 10000
    elif 10000 <= salary and salary < 15000:
        key = 15000
    elif 15000 <= salary and salary < 20000:
        key = 20000
    elif 20000 <= salary and  salary < 25000:
        key = 25000
    else:
        key = 30000
    if key in salary_data.index:
        salary_data[key] += y
    else:
        salary_data[key] = y
    
plt.plot(salary_data.sort_index())
# 设置表，xy轴名称
plt.title("薪资分布-职位数量",fontsize=20)
plt.xlabel("薪资分布",fontsize=15)
plt.ylabel("职位数量",fontsize=15)

plt.savefig(image_path+'salary_positions.png',bbox_inches='tight')

'''公司情况与职位数量关系'''
plt.figure(dpi=128,figsize=(10, 6))
size_posn_obj = df['公司规模'].value_counts() # 获取公司规模数据
financ_posn_obj = df['融资阶段'].value_counts() # 获取融资阶段数据

szp_count_data = list(range(-1,-(len(size_posn_obj.index)+1),-1))
fp_count_data = list(range(1,(len(financ_posn_obj.index)+1)))

szfp_index_data = []
for index in size_posn_obj.index:
    szfp_index_data.append(index)
for index in financ_posn_obj.index:
    szfp_index_data.append(index)

# 公司规模在-y轴 融资阶段在+y轴
plt.barh(szp_count_data,size_posn_obj.values)
plt.barh(fp_count_data,financ_posn_obj.values)
plt.yticks(szp_count_data+fp_count_data,szfp_index_data) # 设置y坐标显示内容
plt.tight_layout()

# 显示每个柱的数据
for x, y in zip(size_posn_obj.values,szp_count_data):
    plt.text(x + 1.5, y, '%s' % x, ha='center', va='center')
for x, y in zip(financ_posn_obj.values,fp_count_data):
    plt.text(x + 1.5, y, '%s' % x, ha='center', va='center')

ax = plt.gca()
ax.xaxis.set_ticks_position('bottom')
ax.spines['right'].set_color('none') # 顶边框
ax.spines['top'].set_color('none') # 右边框
ax.spines['bottom'].set_position(('data', 0))

plt.legend(labels=['公司规模','融资阶段'],loc='best') # 设置图例
plt.title("公司情况-职位数量",fontsize=15) # 设置title
plt.xlim((5,130))
plt.tight_layout()
plt.savefig(image_path+'company_positions.png',bbox_inches='tight')

'''学历、工作经验与职位数量关系'''
plt.figure(dpi=128,figsize=(10, 6))
# 学历 图饼
pie1 = plt.subplot2grid((1, 2), (0, 0))
edu_posn_obj = df['学历'].value_counts()
pie1.pie(edu_posn_obj.values,labels=edu_posn_obj.index,autopct='%3.2f%%',shadow=False,startangle=90,pctdistance=0.6)

# 工作年限 图饼
pie2 = plt.subplot2grid((1, 2), (0, 1))
exp_posn_obj = df['工作年限'].value_counts()
patches, texts = pie2.pie(exp_posn_obj.values,shadow=False,startangle=90,pctdistance=0.6)
exp_posn_sum = np.sum(exp_posn_obj.values)
labels = ['{0} - {1:.2f} %'.format(i,(j/exp_posn_sum)*100) for i,j in zip(exp_posn_obj.index,exp_posn_obj.values)]

plt.legend(patches,labels,loc='right',bbox_to_anchor=(1.1,1.1),fontsize=8) # 设置图例
plt.title("个人情况-职位数量",fontsize=15,x=-0.1,y=1.1) # 设置title

plt.savefig(image_path+'person_info_positions.png',bbox_inches='tight')

plt.show()