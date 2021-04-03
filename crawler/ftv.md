import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime
import os
from random import randint
from time import sleep
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

for k in range(1,201):
    url  = f'https://www.ftvnews.com.tw/tag/%e6%94%bf%e6%b2%bb/{k}'
    res  = requests.get(url,headers=headers)
    soup = BeautifulSoup(res.text,'lxml')
    links = soup.select('ul.row > li > a')
    try:
        for i in links:
            link=i.get('href')
            url=f'https://www.ftvnews.com.tw/{link}'
            resp = requests.get(url,headers=headers)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text,'html.parser')
                title= soup.select('h1.text-center')[0].text
                content='\n'.join(i.text for i in soup.find('div',attrs={'id':'newscontent'}).find_all('p'))
    except:
        pass
columns = ['TITLE','CONTENT']
df = pd.DataFrame(data=data, columns=columns)
df.to_csv('ftv.csv',index=False,encoding='utf-8')
