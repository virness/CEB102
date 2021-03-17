Pchome爬蟲  這篇是教大家怎麼把資料爬下來存在csv然後匯入pymysql

import requests
import json
import pandas as pd
import pymysql
def pchome(keyword):

        url=f'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={keyword}&page=2&scope=all'
        data=requests.get(url).text
        jsondata=json.loads(data)
        products=jsondata['prods']
        data=[]
        for i in products:
                if float(i['price'])>10000:
                    url=str('https://24h.pchome.com.tw/prod/'+i['Id'])
                    name=str(i['name'])
                    price=str(i['price'])            
                    content=str(i['describe'][:100])
                    pic1='https://b.ecimg.tw/'+str(i['picS'])
                    pic2='https://b.ecimg.tw/'+str(i['picB'])                    
  
                    data.append([url,name,price,content,pic1,pic2])

        columns=['商品網址','商品名稱','價格','商品內容','圖片1','圖片2']                     #第一欄的名稱
        df = pd.DataFrame(data=data, columns=columns)
        df.to_csv(r'./pchome.csv',index=False,encoding='utf-8-sig')
        
--------------------------------------------------------------------------------------------------------------

keyword = input("請輸入關鍵字:") 
keyword = keyword.replace(" ","&")
pchome(keyword)


--------------------------------------------------------------------------------------------------------------

import pandas as pd
from sqlalchemy import create_engine

# 初始化資料庫連線，使用pymysql模組
engine = create_engine('mysql+pymysql://root:(密碼)@localhost/(資料庫名稱)?charset=utf8')
# 讀取本地CSV檔案
df = pd.read_csv("pchome.csv", sep=',')
# 將新建的DataFrame儲存為MySQL中的資料表，不儲存index列
df.to_sql('pchome', engine, index= False)
print("Write to MySQL successfully!")
