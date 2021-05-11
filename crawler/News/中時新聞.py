#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
for i in range(1,4):
    for j in range(1,32):
        for k in range(0,5000):
            url = 'https://www.chinatimes.com/realtimenews/20210{}{}00{}-260407?chdtv'.format(i,j,("%03d" % (k)))
            resp = requests.get(url,headers=headers)
            try:
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text,'html.parser')
                    url = soup.find('link')['href']
                    ndf = pd.DataFrame(data = [{'TITLE':soup.find('h1', attrs={'class':'article-title'}).text,
                                                'TIME':datetime.strptime(soup.find('meta', attrs={'property':'article:published_time'})['content'],'%Y-%m-%dT%H:%M:%S+08:00'),
                                                'CONTENT':'\n'.join(i.text for i in soup.find('div',attrs={'class':'article-body'}).find_all('p')),
                                                'FROM':soup.find('meta',{'name':'publisher'})['content']}],
                                       columns = ['TITLE', 'TIME','CONTENT','FROM']) 
                    time.sleep(1)
                    df.to_csv(r'./news.csv',index=False,encoding='utf-8-sig')
            except:
                pass
                
存入mysql



import pandas as pd from sqlalchemy import create_engine

# 初始化資料庫連線，使用pymysql模組

engine = create_engine('mysql+pymysql://root:(密碼)@localhost/(資料庫名稱)?charset=utf8')

# 讀取本地CSV檔案

df = pd.read_csv("news.csv", sep=',')

# 將新建的DataFrame儲存為MySQL中的資料表，不儲存index列

df.to_sql('chinesenews', engine, index= False) print("Write to MySQL successfully!")

