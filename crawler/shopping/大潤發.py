#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
from bs4 import BeautifulSoup

rsp = requests.get('https://www.rt-mart.com.tw/direct/')
soup = BeautifulSoup(rsp.text, 'lxml')

try:
    if resp.status_code == 200:
    for li in soup.select('li.nav01 h4 a'):
    data=[]
    url = 'https://www.rt-mart.com.tw/direct/'+li.get('href')
    res=requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    for item in soup.select('h5.for_proname a'):
    url = item.get('href')
    res=requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    title=soup.select('span.h2')[0].text
    price=soup.select('span.price_num')[0].text
    content=soup.select('div.TxtContent')[0].text
    data.append([title,price,content])
    sleep_time = random.randint(3,10)
    print("sleep time: %s sec"%(sleep_time))
    time.sleep(sleep_time)

    for li in soup.select('li.nav02 h4 a'):  
            data1=[]  
            url = 'https://www.rt-mart.com.tw/direct/'+li.get('href')  
            res=requests.get(url)  
            soup = BeautifulSoup(res.text, 'lxml')  
            for item in soup.select('h5.for_proname a'):  
                url = item.get('href')  
                res=requests.get(url)  
                soup = BeautifulSoup(res.text, 'lxml')  
                title=soup.select('span.h2')[0].text  
                price=soup.select('span.price_num')[0].text  
                content=soup.select('div.TxtContent')[0].text  
                data1.append([title,price,content])  
                sleep_time = random.randint(3,10)  
                print("sleep time: %s sec"%(sleep_time))  
                time.sleep(sleep_time)  
except:
pass
columns = ['商品名稱','價格','商品介紹']
df = pd.DataFrame(data=[data,data1],columns=columns)
df.to_csv('Market.csv',index=False,encoding='utf-8-sig')

import pandas as pd from sqlalchemy import create_engine

初始化資料庫連線，使用pymysql模組

engine = create_engine('mysql+pymysql://root:(密碼)@localhost/(資料庫名稱)?charset=utf8')

讀取本地CSV檔案

df = pd.read_csv("Market.csv", sep=',')

將新建的DataFrame儲存為MySQL中的資料表，不儲存index列

df.to_sql('market', engine, index= False) print("Write to MySQL successfully!")

