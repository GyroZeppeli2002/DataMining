import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import openpyxl

# 解决中文乱码问题
plt.rcParams['font.sans-serif'] = 'SimHei'
# 解决负号无法显示问题
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_excel('D:/PyCharm/AssessmentProject_for_Fds/数据获取/data.xlsx')
df.rename(columns={'Unnamed: 0': 'id'}, inplace=True)
# df1 = df.drop(columns=['id', '商品名称', '图片', ], axis=1)
# # 价格分箱：0-500,500-1000，1000-2000,2000-3000,3000-4000,4000-5000,5000-10000
# df1['价格分箱'] = pd.cut(df1['价格'], bins=[0, 500, 1000, 2000, 3000, 4000, 5000, 10000])
# #print(df1)
# price_stats = df1['价格分箱'].value_counts()
# #print(price_stats)
# plt.figure(figsize=(10,5))
# plt.pie(price_stats.values,labels=price_stats.index,startangle=90,autopct='%.2f%%',)
# plt.title('价格区间分布饼图(单位：元)')
# plt.legend()
# plt.show()
# # 保存图片

# plt.figure(figsize=(10,5))
# plt.hist(df['价格'],bins=20,color='b',edgecolor='k',alpha=0.3)
# plt.title('价格分布直方图')
# plt.show()

# plt.figure(figsize=(10,5))
# x = df['价格']
# y = df['好评率']
# plt.scatter(x,y,color='r')
# plt.title('价格好评率散点图')
# plt.xlabel('价格')
# plt.ylabel('好评率')
# plt.savefig()



# df2 = pd.read_excel('D:/PyCharm/AssessmentProject_for_Fds/数据获取/data_code01.xlsx''')
# X = df2[['价格','好评率','差评率','评论数编码']]
# corr = X.corr()
# plt.figure(figsize=(6,6))
# sns.heatmap(corr,
#             annot=True,  # 显示相关系数的数据
#             center=0.5,  # 居中
#             fmt='.2f',  # 只显示两位小数
#             linewidth=0.2,  # 设置每个单元格的距离
#             linecolor='blue',  # 设置间距线的颜色
#             vmin=0, vmax=1,  # 设置数值最小值和最大值
#             xticklabels=True, yticklabels=True,  # 显示x轴和y轴
#             square=True,  # 每个方格都是正方形
#             cbar=True,  # 绘制颜色条
#             cmap='coolwarm_r',  # 设置热力图颜色
#             )
# plt.show()
# from sklearn.preprocessing import LabelEncoder
# from sklearn.preprocessing import Normalizer
# from sklearn.cluster import KMeans
# from sklearn.metrics import silhouette_score
# from sklearn import preprocessing
# from sklearn import metrics
# import category_encoders as ce
#
# df1 = df[['价格','CPU类型','最大充电功率','最大运行内存(GB)','最大机身内存(GB)','后摄主像素(千万)']]
#
# df1['最大充电功率'] = df1['最大充电功率'].astype('str')
# df1['最大运行内存(GB)'] = df1['最大运行内存(GB)'].astype('str')
# df1['最大机身内存(GB)'] = df1['最大机身内存(GB)'].astype('str')
# df1['后摄主像素(千万)'] = df1['后摄主像素(千万)'].astype('str')
#
# map1 = [
#     {'col':'CPU类型','mapping':{'其他':0,'骁龙7系列':500,'天玑700系列':600,'天玑800系列':700,'天玑900系列':800,'天玑7000系列':900,'天玑8000系列':1000,'骁龙8系列':1100,'麒麟9系列':1200,'天玑9000系列':1300,'苹果A系列':1800}},
#     {'col':'最大充电功率','mapping':{'以官网信息为准':225,'25':250,'49':490,'79':790,'119':1190,'150':1500,'200':2000,'240':2400}},
#     {'col':'最大运行内存(GB)','mapping':{'3':300,'4':400,'6':600,'未公布':700,'8':800,'12':1200,'16':1600,'18':1800,'24':2400}},
#     {'col':'最大机身内存(GB)','mapping':{'nan':0,'1':10,'32':320,'未公布':480,'64':640,'128':1280,'256':2560,'512':5120}},
#     {'col':'后摄主像素(千万)','mapping':{'0':0,'普通(以官网信息为准)':100,'1.2':120,'1.3':130,'1.6':160,'4':400,'4.8':480,'5':500,'5.4':540,'6.4':640,'10':1000,'20':2000}}
# ]
#
# encoder = ce.OrdinalEncoder(cols=['CPU类型','最大充电功率','最大运行内存(GB)','最大机身内存(GB)','后摄主像素(千万)'],return_df=True,mapping=map1)
# cancerdata_transformed = encoder.fit_transform(df1)
# cancerdata_transformed['价格'] = df1['价格']
#
# # Label = LabelEncoder()
# # df1['CPU编码'] = Label.fit_transform(df1['CPU类型'])
# # df1['功率编码'] = Label.fit_transform(df1['最大充电功率'])
# # df1['运行内存编码'] = Label.fit_transform(df1['最大运行内存(GB)'])
# # df1['机身内存编码'] = Label.fit_transform(df1['最大机身内存(GB)'])
# # df1['后摄编码'] = Label.fit_transform(df1['后摄主像素(千万)'])
# #
# # X = df1[['价格','CPU编码', '功率编码', '运行内存编码', '机身内存编码', '后摄编码']]
# NL = Normalizer()
# X = NL.fit_transform(cancerdata_transformed)
# score = []
# # 初始化聚类个数2到10个
# range_values = np.arange(2, 11)
# # 循环训练簇的个数从2到10的模型，计算每个模型的轮廓系数
# for i in range_values:
#     kmenas = KMeans(n_clusters=i)
#     kmenas.fit(X)
#     s = silhouette_score(X, kmenas.labels_)
#     score.append(s)
# # 通过观察，分3类，得分最高
# plt.bar(range_values, score, width=0.7, color='r', align='center')
# plt.show()
# kmenas = KMeans(n_clusters=2)
# kmenas.fit(X)
# y_pred = kmenas.labels_
# # print(y_pred)
#
#
# center = kmenas.cluster_centers_
# df2 = pd.DataFrame(center,columns=[['价格','CPU', '功率', '运行内存', '机身内存', '后摄']])
# # print(df1)
# df2.plot(kind='bar')
# plt.xticks(rotation=360)
# plt.show()
#
# # df1['类别'] = y_pred
# # df1.to_excel('手机分类.xlsx')

# df = pd.read_excel('手机分类.xlsx')
# # 出点击的房源属于哪个找分类
# label = df[df['Unnamed: 0'] == id]['类别'].values[0]
# # 取出此分类所有记录
# data = df[df['类别'] == label]
# # 随机选取5条作为推荐房源
# df_res = data.sample(5)
# # 把dataframe转换成字典列表
# goods_list = df_res.to_dict(orient='records')
# print(goods_list)

