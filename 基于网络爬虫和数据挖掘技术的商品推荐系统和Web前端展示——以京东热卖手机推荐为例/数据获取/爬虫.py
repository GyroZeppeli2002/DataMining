import requests
from lxml import html
import time
import pandas as pd
import openpyxl
import pymysql

# conn = pymysql.connect(host='localhost',port=3306,user='root',passwd='123456',db='京东',charset='utf8')
# cursor = conn.cursor()

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Cookie':'__jdu=1700211823334798743723; shshshfpa=5b9d151d-f466-4e6e-09cd-0e7c3ca624c4-1700211824; shshshfpx=5b9d151d-f466-4e6e-09cd-0e7c3ca624c4-1700211824; PCSYCityID=CN_320000_320100_0; TrackID=1KygnYOTh39Nu9vB73lSOSJtpE7Q2fE5y897KUzO8ClqxHKu5pvejVmtojK4g7xazyNMNgZdIvPymUZb3fNHIeLF_JiKBwvQFkyD_HkXaNuMVUF8yqkr1eI5KBG6qICTT; thor=C8E6DDB81BCC0AA2BFD3790A308D1BA83EF77A1B54AEC19DF0E4397076E3BE8A1FD9D606BC17537380492D1D93EF77EAAEC8A47C4342AC6CD9FB91559AFAE91EE60418A4AA3358C1D7011039489236BAFBD777F30B02A58D9BF63992E233F1316ACE663D6C1A22674EF064D18B24B3837170CD9922DD5AD2D2AC1BF8203339779BDAA01465907AF9301F033A384826264DBB87E0C6B81DE53B14D497E44F9AB5; flash=2_KmjJjbdf92uPyublF1XvdM9tNNSBTj_KI3vh10EHv0gTMMDADPN7tRhQaL8DtIFG66vm4lJeKvNMQNGp9sWlOuyYtjPea0iLxeD8CN5PQoq*; pinId=ni4aq7X4n7VR1PE9rbqkfA; pin=jd_wWcdTZLjvsar; unick=jd_wWcdTZLjvsar; _tp=Brx9JbNTyI93o4dC6BS%2BpQ%3D%3D; _pst=jd_wWcdTZLjvsar; areaId=12; ipLoc-djd=12-904-907-50559; user-key=3c049755-6d27-4591-9eb7-2b911fcb628c; jsavif=0; mba_muid=1700211823334798743723; jsavif=0; unpl=JF8EAKNnNSttWU1RARtVTEZCS1VQW14MH0cCPzdWXQ9QGQQMEwFLG0d7XlVdXxRLFB9vYRRUWFNLUg4eCysSEXteVV5dD04eBGljNWRtW0tkBCsCHRMRSF1UV14KSRUGaW8MUlhaTVcHKwMrEhhPbWRuWAhKFwNuYwFQWWhKZAQrVHUSEUpcVFlYAE4XTm9hBFVeWEtdBhkAGRcWQ1RSW18OSBUzblcG; __jdv=188976424|cs.hae123.cn|t_2011648675_|tuiguang|07451ffec195425ea0aab8c9ca892a8f|1702793868238; cn=2; 3AB9D23F7A4B3C9B=NH3Q34QELGPUILZO43XWQHCQMDCISXKEHE56NPDKGZIV7DKSODYDQZVF7NFSOG6OHTQTRLVPS35SYHP2DLLT3SY6N4; __jda=181111935.1700211823334798743723.1700211823.1702785004.1702788637.11; __jdc=181111935; token=163922534f2530310e3aba31e466e1ee,3,945997; __tk=qUNY2UV51DytKUyu1YS4rAsE1YxE2za41YqB2UrsrcM4KwfDrwtu2G,3,945997; mba_sid=17027888816364694817906515623.87; __jd_ref_cls=LoginDisposition_Go; x-rp-evtoken=N-nAb5Oj6OS1u8hkvixIgGQhIqsLIwkjaiyEuOnMzZAqJfwTmIs3EyfubzElSbDIpO1utr4fKDKrj3QEV22STZVfKyxVi_1W_3u3TSA83ZDeEI2aw2MoOafpHBdi5IO5YCUOlttL7PPHJYuuuQ9bjPI1Yfk6-sr7WwgFp9ho8ft8V_l7DeBHmxkUTFy2pfCTnYR5BlcyqSuvmmiJa7dR7vqvR36FhIJFpiT-jKx1rlE%3D; 3AB9D23F7A4B3CSS=jdd03NH3Q34QELGPUILZO43XWQHCQMDCISXKEHE56NPDKGZIV7DKSODYDQZVF7NFSOG6OHTQTRLVPS35SYHP2DLLT3SY6N4AAAAMMO2HFVFIAAAAAD747UQNFAC47JYX; _gia_d=1; shshshsID=7072fc051b29482ce2944a205cc07f9b_2547_1702796087982; __jdb=181111935.2711.1700211823334798743723|11.1702788637; shshshfpb=AAmZbjnaMEp0VHfRmTm4JzQ58PKYkxBcAIRgkfwAAAAA'
}

# 从详情页获取商品名称
name_list = []
# 缩略页图片链接
img_list = []
# 缩略页获取价格
price_list = []
# 从详情页获取COU型号
cpu_list = []
# 运行内存
RAM_list = []
# 机身内存
ROM_list = []
# 充电功率
charge_list = []
# 后摄主像素
camera_list = []
# 商品编号
id_list = []
# 累计评论:
comment_list = []
# 好评率
goodrate_list = []
# 差评率
poorrate_list = []

s = 0
for i in range(0,1):
    print(f'开始爬第{i+1}页')
    page = i*2 + 1
    if page==1:
        s = 1
    elif page==2:
        s = 56
    else:
        s = s + 60

    url = f'https://search.jd.com/Search?keyword=手机&page={page}&s={s}'

    response = requests.get(url,headers=headers)
    page_text = response.text
    etree = html.etree
    tree = etree.HTML(page_text)

    # 爬取缩略页
    li_list = tree.xpath('//li[@class="gl-item"]')
    li = li_list[0]

    # 获取详情页链接
    detail = li.xpath('//div[@class="p-img"]/a/@href')
    detail_url_list = ['https:' + i for i in detail]

    # 获取图片链接
    pic = li.xpath('//div[@class="p-img"]/a/img/@data-lazy-img')
    pic_list = ['https:' + i for i in pic]
    img_list.extend(pic_list)

    # 获取价格
    price_list.extend(li.xpath('//div[@class="p-price"]/strong/i/text()'))

    # 访问详情页
    for d_url in detail_url_list:

        response = requests.get(d_url,headers=headers)
        page_text = response.text
        tree = etree.HTML(page_text)

        # 爬取详情页基础信息
        property_list = tree.xpath('//ul[@class="parameter2 p-parameter-list"]/li/text()')
        dict = {}
        for item in property_list:
            p = item.split('：')
            # print(s)
            if len(p) == 2:
                dict[p[0]] = p[1]
        name_list.append(dict.get('商品名称', ''))
        cpu_list.append(dict.get('CPU型号', ''))
        RAM_list.append(dict.get('运行内存', ''))
        ROM_list.append(dict.get('机身内存', ''))
        charge_list.append(dict.get('充电功率', ''))
        camera_list.append(dict.get('后摄主像素'))

        # 爬取和评论有关的信息
        id_list.append(dict.get('商品编号',''))
        # 生成时间戳
        t = str(time.time())
        t = t[0:-4]
        list = t.split('.')
        t = list[0] + list[1]

        # jsonpath爬虫
        url1 = f'https://api.m.jd.com/?appid=item-v3&functionId=pc_club_productCommentSummaries&client=pc&clientVersion=1.0.0&t={t}&referenceIds={id_list[-1]}&categoryIds=9987%2C653%2C655&loginType=3&bbtf=&shield=&uuid=181111935.1700211823334798743723.1700211823.1702733119.1702736447.9'
        response = requests.get(url1,headers=headers)
        page_text1 =response.text
        import json
        dict1 = json.loads(page_text1)
        dict1 = dict1.get("CommentsCount","")[0]
        comment_list.append(dict1.get("CommentCountStr",""))
        goodrate_list.append(dict1.get("GoodRate",""))
        poorrate_list.append(dict1.get("PoorRate",""))

        # try:
        #     sql = 'insert into hire(商品名称,图片,价格,CPU,运行内存,机身内存,充电功率,后摄主像素,累计评论数,好评率，差评率) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        #     val = (
        #         name_list[-1],
        #         img_list[-1],
        #         price_list[-1],
        #         cpu_list[-1],
        #         RAM_list[-1],
        #         ROM_list[-1],
        #         charge_list[-1],
        #         camera_list[-1],
        #         comment_list[-1],
        #         goodrate_list[-1],
        #         poorrate_list[-1]
        #     )
        #     cursor.execute(sql, val)
        #     conn.commit()
        # except Exception as e:
        #     print(e)

        time.sleep(2)

    print(f"第{i+1}页已经完成")
    time.sleep(15)

# 整理输出
dataset = {
    "商品名称":name_list,
    "图片":img_list,
    "价格":price_list,
    "CPU":cpu_list,
    "运行内存":RAM_list,
    "机身内存":ROM_list,
    "充电功率":charge_list,
    "后摄主像素":camera_list,
    "累计评论数":comment_list,
    "好评率":goodrate_list,
    "差评率":poorrate_list,
}

df = pd.DataFrame(dataset)
df.to_excel('test.xlsx',index=False)




