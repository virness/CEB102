import requests
import json
from bs4 import BeautifulSoup
import csv
import pandas as pd

userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
headers ={'User-Agent':userAgent}

ss = requests.session()

data = [] #把取得的資訊都放入list

def songo(keyword):

    userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    headers ={'User-Agent':userAgent}
    url = f'https://www.pcone.com.tw/search?q={keyword}&sortBy=price&sortDir=desc'
    res = ss.get(url,headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')
    links = soup.select('a.product-list-item')  #取出這一頁所有職位的網址

    for link in links:
            link = link["href"].split("?")[0].split("&sort")[-1]
            headers= {'User-Agent': userAgent,}        
            res = 'https://www.pcone.com.tw'+str(link)
            res =ss.get(res,headers=headers)
            soup =BeautifulSoup(res.text,'html.parser')

            name = soup.select('h1.product-name')[0].text
            price= soup.select('span.bind-lowest-price.discount')[0].text
            link = 'https://www.pcone.com.tw' + str(link)
            pic  = ''
            data.append([name,price,link])
    columns=['商品名稱','商品價格','商品連結']                     #第一欄的名稱
    df = pd.DataFrame(data=data, columns=columns)
    df.to_csv(r'./songo.csv',index=False,encoding='utf-8-sig')
    
------------------------------------------------------------------------------------------------------------
    
keyword = input("請輸入關鍵字:") 
keyword = keyword.replace(" ","&")
songo(keyword)

------------------------------------------------------------------------------------------------------------

import pandas as pd
from sqlalchemy import create_engine

初始化資料庫連線，使用pymysql模組

engine = create_engine('mysql+pymysql://root:a9534068@localhost/stock?charset=utf8')

讀取本地CSV檔案

df = pd.read_csv("songo.csv", sep=',')

將新建的DataFrame儲存為MySQL中的資料表，不儲存index列

df.to_sql('songo', engine, index= False)
print("Write to MySQL successfully!")
