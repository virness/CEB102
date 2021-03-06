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
for i in range(1880000,1951609):
    url = f'https://www.ettoday.net/news/20200107/{i}.htm'
    resp = requests.get(url,headers=headers)
    try:
        if resp.status_code == 200:
                soup = BeautifulSoup(resp.text,'html.parser')
                cate= soup.find('meta', attrs={'property':'article:section'})['content']
                time=soup.find('time',attrs={'class':'date'}).text
                content='\n'.join(i.text for i in soup.find('div',attrs={'class':'story'}).find_all('p'))
                data.append([cate,time,content])
                sleep_time = random.randint(3,10)
                print("sleep time: %s sec"%(sleep_time))
                time.sleep(sleep_time)
    except:
        pass            
columns = ['Cate','TIME','CONTENT']
df = pd.DataFrame(data=data, columns=columns)
df.to_csv('ettodaynews.csv',index=False,encoding='utf-8-sig')

