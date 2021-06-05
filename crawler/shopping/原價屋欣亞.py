#!/usr/bin/env python
# coding: utf-8

# In[15]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
# from sqlalchemy import create_engine
import json

# engine = create_engine('mysql+pymysql://root:123456@localhost/stock?charset=utf8')
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


# In[5]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:123456@localhost/stock?charset=utf8')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
url='https://www.coolpc.com.tw/evaluate.php'
res=requests.get(url,headers=headers)
soup=BeautifulSoup(res.text,'html.parser')

data=[]
for i in soup.find('select',{'onchange':'cnt(5)'}) .select('optgroup')[0].select('option'):
    try:
        a=i['disabled']
        i.extract()
    except:
        total=i.text
        data.append([total])
for i in soup.find('select',{'onchange':'cnt(6)'}) .select('optgroup')[0].select('option'):
    try:
        a=i['disabled']
        i.extract()
    except:
        total=i.text
        data.append([total])
for i in soup.find('select',{'onchange':'cnt(7)'}) .select('optgroup')[0].select('option'):
    try:
        a=i['disabled']
        i.extract()
    except:
        total=i.text
        data.append([total])
for i in soup.find('select',{'onchange':'cnt(11)'}) .select('optgroup')[0].select('option'):
    try:
        a=i['disabled']
        i.extract()
    except:
        total=i.text
        data.append([total])

for i in soup.find('select',{'onchange':'cnt(12)'}) .select('optgroup')[0].select('option'):
    try:
        a=i['disabled']
        i.extract()
    except:
        cpu=i.text
        data.append([total])
for i in soup.find('select',{'onchange':'cnt(13)'}) .select('optgroup')[0].select('option'):
    try:
        a=i['disabled']
        i.extract()
    except:
        total=i.text
        data.append([total])
for i in soup.find('select',{'onchange':'cnt(14)'}) .select('optgroup')[0].select('option'):
    try:
        a=i['disabled']
        i.extract()
    except:
        total=i.text
        data.append([total])
for i in soup.find('select',{'onchange':'cnt(15)'}) .select('optgroup')[0].select('option'):
    try:
        a=i['disabled']
        i.extract()
    except:
        total=i.text
        data.append([total])
        
columns=['product']
df=pd.DataFrame(data=data,columns=columns)
df.reset_index(inplace=False)
df.to_sql('coolpc', engine, index= False,if_exists='replace')

