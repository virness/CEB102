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
import time
import random

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
data=[]
for i in range(860000,890000):
    url = f'https://www.setn.com/News.aspx?NewsID={i}&utm_source=setn.com&utm_medium=viewall&utm_campaign=viewallnews'
    resp = requests.get(url,headers=headers)
    try:
        if resp.status_code == 200:
                soup = BeautifulSoup(resp.text,'html.parser')
                cate   = soup.find('meta', attrs={'property':'article:section'})['content'] 
                title=soup.find('h1', attrs={'class':'news-title-3'}).text
                time=soup.find('time',attrs={'class':'page-date'}).text
                content='\n'.join(i.text for i in soup.find('div',attrs={'id':'Content1'}).find_all('p'))
                data.append([cate,title,content])
                sleep_time = random.randint(3,10)
                print("sleep time: %s sec"%(sleep_time))
                time.sleep(sleep_time)
    except:
        pass
columns = ['Cate','TITLE','CONTENT']
df = pd.DataFrame(data=data, columns=columns)
df.to_csv('sentnews.csv',index=False,encoding='utf-8-sig')

---------------------------------------------------------------------------------------------------------------------
import pandas as pd from sqlalchemy import create_engine

# 初始化資料庫連線，使用pymysql模組

engine = create_engine('mysql+pymysql://root:(密碼)@localhost/(資料庫名稱)?charset=utf8')

# 讀取本地CSV檔案

df = pd.read_csv("setnews.csv", sep=',')

# 將新建的DataFrame儲存為MySQL中的資料表，不儲存index列

df.to_sql('setnews', engine, index= False) print("Write to MySQL successfully!")

