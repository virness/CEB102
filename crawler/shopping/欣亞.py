#!/usr/bin/env python
# coding: utf-8

# In[15]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import json


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
url='https://www.sinya.com.tw/diy/api_prods'
res=requests.get(url,headers=headers).text
jsondata=json.loads(res)
data=[]
for i in jsondata:
    if i['price'] == "0":
        continue
    elif i['stockText'] =="":
        name =i['prod_name']
        price=i['price']
        data.append([name,price])
        
columns=['product','price']
df = pd.DataFrame(data=data, columns=columns)
# df.to_sql('sinya', engine, index= False,if_exists='replace')
df.to_csv('sinya.csv',encoding='utf-8-sig')
