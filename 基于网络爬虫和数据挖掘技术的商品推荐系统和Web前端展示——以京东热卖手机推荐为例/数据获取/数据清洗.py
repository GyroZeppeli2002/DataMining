import pandas as pd
import openpyxl
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# 导入数据
df = pd.read_excel('./dataset.xlsx')
#print(df.info)

# 删除没有图片的个体
df['图片'] = df['图片'].str.strip()
df = df[df['图片'] != '']

# 用“未公布”填补CPU、运行内存、机身内存的缺失值
df['CPU'].fillna('未公布',inplace=True)
df['运行内存'].fillna('未公布',inplace=True)
df['机身内存'].fillna('未公布',inplace=True)
# 用“以官网信息为准”填补充电功率的缺失值
df['充电功率'].fillna('以官网信息为准',inplace=True)
# 用“普通(以官网信息为准)”填补后摄主像素缺失值
df['后摄主像素'].fillna('普通(以官网信息为准)',inplace=True)

# 检查有无缺失值
#print(df.isnull().sum().sort_values(ascending=False))

# 忽略前两列
#df1 = df.drop(['商品名称','图片'],axis=1)

# 利用正则表达式对CPU重新分类
#print(df['CPU'].value_counts())
import re
cpu_categories = {
    '天玑9000系列':r'天玑9\d{3,}[^_]*',
    '天玑8000系列':r'天玑8\d{3,}[^_]*',
    '天玑7000系列':r'天玑7\d{3,}[^_]*',
    '天玑900系列':r'天玑9\d{2}[^_]*',
    '天玑800系列':r'天玑8\d{2}[^_]*',
    '天玑700系列':r'天玑7\d{2}[^_]*',
    '骁龙8系列':r'骁龙8',
    '骁龙7系列':r'骁龙7',
    '麒麟9系列': r'麒麟9',
    '苹果A系列': r'A',
}
def categorize_processor(processor):
    for category, pattern in cpu_categories.items():
        if re.search(pattern, processor):
            return category
    return '其他'  # 如果没有匹配到任何类别，则归为'Other'
df['CPU类型'] = df['CPU'].apply(categorize_processor)

# 利用正则表达式获取最大充电功率
#print(df['充电功率'].value_counts())
def extract_max_power(description):
    # 处理未知值
    if description == '以官网信息为准':
        return '以官网信息为准'
    # 提取数字范围的上限
    match = re.search(r'(\d+)-(\d+)W', description)
    if match:
        return int(match.group(2))
    # 对于单一数值的描述
    match_single = re.search(r'(\d+)W及以下', description)
    if match_single:
        return int(match_single.group(1))
    # 处理特殊情况
    match_single_value = re.search(r'(\d+)W', description)
    if match_single_value:
        return int(match_single_value.group(1))
# 应用函数到 '充电功率' 列
df['最大充电功率'] = df['充电功率'].apply(extract_max_power)

#利用正则表达式整理运行内存和机身内存
#print(df['运行内存'].value_counts())
def extract_memory (description):
    if description == '未公布':
        return '未公布'
    match = re.search(r'(\d+)',description)
    if match :
        return int(match.group())
df['最大运行内存(GB)'] = df['运行内存'].apply(extract_memory)
df['最大机身内存(GB)'] = df['机身内存'].apply(extract_memory)

# 利用正则表达式对后置摄像头数据进行更改
#print(df['后摄主像素'].value_counts())
def reset_camare(description):
    if description == '普通(以官网信息为准)' or description == '未上市':
        return '普通(以官网信息为准)'
    elif description == '无后置摄像头':
        return 0
    match = re.search(r"(\d+)",description)
    # 亿级
    if int(match.group()) < 10:
        return int(match.group())*10.0
    # 千万级
    else:
        return int(match.group())/1000.0
df['后摄主像素(千万)'] = df['后摄主像素'].apply(reset_camare)

# 利用正则表达式处理累计评论数:
# print(df['累计评论数'].value_counts())
def extract_comment_count(description):
    description = str(description)
    # 处理未知值
    if description == '未知':
        return None

    # 提取数字，并去掉 "万" 和 "+"
    match = re.search(r'(\d+)万\+', description)
    match_single = re.search(r'(\d+)\+', description)

    if match:
        if int(match.group(1)) < 10:
            return "1-10万"
        elif 10 <= int(match.group(1)) < 60:
            return "10-60万"
        else:
            return "60万以上"

    # 对于直接数字的情况，去掉 "+"

    elif match_single:
        if int(match_single.group(1)) < 500:
            return "不足500条"
        elif 500 <= int(match_single.group(1)) < 4000:
            return "500-4000条"
        else:
            return "4000-10000条"
    else:
        return "不足500条"
# 应用函数到 '评论数' 列
df['评论数'] = df['累计评论数'].apply(extract_comment_count)

# print(len(df),end='\n')
# print(len(df['后摄主像素(千万)']),end='\n')
# print(len(df['最大运行内存(GB)']),end='\n')
# print(len(df['最大机身内存(GB)']),end='\n')
# print(len(df['最大充电功率']),end='\n')
# print(len(df['CPU类型']),end='\n')

df1 = df.drop(['运行内存','机身内存','充电功率','CPU',"后摄主像素"],axis=1)
df1.to_excel('data.xlsx',index=True)

# 对评论数进行数据编码化--便于热力图相关性分析和聚类分析
df2 = df1[['价格','好评率','差评率']]
df2['评论数'] = df['累计评论数']
def extract_comment_count_code(description):
    description = str(description)
    # 处理未知值
    if description == '未知':
        return None

    # 提取数字，并去掉 "万" 和 "+"
    match = re.search(r'(\d+)万\+', description)
    match_single = re.search(r'(\d+)\+', description)

    if match:
        if int(match.group(1)) < 10:
            return 10
        elif 10 <= int(match.group(1)) < 60:
            return 20
        else:
            return 50

    # 对于直接数字的情况，去掉 "+"

    elif match_single:
        if int(match_single.group(1)) < 500:
            return 0
        elif 500 <= int(match_single.group(1)) < 4000:
            return 1
        else:
            return 1.5
    else:
        return 0
df2['评论数编码'] = df2['评论数'].apply(extract_comment_count_code)
df2.to_excel('data_code01.xlsx',index=True)



