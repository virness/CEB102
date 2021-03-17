#momo 購物網
#第一部分先導入所需的套件

from bs4 import BeautifulSoup 
import requests
import re

建立一個 headers避免被擋住ip
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

建立函數
def momo(keyword):
    url=f'https://m.momoshop.com.tw/search.momo?searchKeyword={keyword}&couponSeq=&searchType=3&cateLevel=-1&curPage=1&cateCode=&cateName=&maxPage=228&minPage=1&_advCp=N&_advFirst=N&_advFreeze=N&_advSuperstore=N&_advTvShop=N&_advTomorrow=N&_advNAM=N&_advStock=N&_advPrefere=N&_advThreeHours=N&_advPriceS=&_advPriceE=&_brandNameList=&_brandNoList=&ent=b&_imgSH=fourCardType&specialGoodsType=&_isFuzzy=0&_spAttL=&_mAttL=&_sAttL=&_noAttL='
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text)
        for item in soup.select('li.goodsItemLi > a'):
            urls.append('https://m.momoshop.com.tw'+item['href'])


    data = []
    for i, url in enumerate(urls):
        columns = []
        values = []

        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.text)
        # 標題
        title = soup.find('meta',{'property':'og:title'})['content']
        # 連結
        link = soup.find('meta',{'property':'og:url'})['content']
        # 特價
        amount = soup.find('meta',{'property':'product:price:amount'})['content']
        # 圖片
        img =soup.find('meta',{'property':'og:image'})['content']
        desc = soup.find('div',{'class':'Area101'}).text
        desc = re.sub('\r|\n| ', '', desc)
        desc =str(desc)[:200]
        data.append([title,link,img,amount,desc])
    
    columns=['商品名稱','商品連結','圖片','價格','商品內容']                     #第一欄的名稱
    df = pd.DataFrame(data=data, columns=columns)
    df.to_csv(r'./momo.csv',index=False,encoding='utf-8-sig')
    
--------------------------------------------------------------------------------------------------------------------------------------------    
    
keyword = input("請輸入關鍵字:") 
keyword = keyword.replace(" ","+")
momo(keyword)

--------------------------------------------------------------------------------------------------------------------------------------------
import pandas as pd
from sqlalchemy import create_engine

初始化資料庫連線，使用pymysql模組
engine = create_engine('mysql+pymysql://root:<password>@localhost/<data name>?charset=utf8')
讀取本地CSV檔案
df = pd.read_csv("momo.csv", sep=',')
將新建的DataFrame儲存為MySQL中的資料表，不儲存index列
存入的table叫做momo 不須額外設定格式
df.to_sql('momo', engine, index= False)
print("Write to MySQL successfully!")
