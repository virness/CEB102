#請先下載台股代號  下載後在stock_id.csv可以看到台股代號 將其他欄位全部刪除即可

import requests
import numpy as np
import pandas as pd

link = 'https://quality.data.gov.tw/dq_download_json.php?nid=11549&md5_url=bb878d47ffbe7b83bfc1b41d0b24946e'
r = requests.get(link)
data = pd.DataFrame(r.json())

data.to_csv('stock_id.csv', index=False, header = True,encoding='utf-8-sig')

---------------------------------------------------------------------------------------------------------

#這邊我們要用yahoo爬蟲套件請先安裝

!pip install yfinance
---------------------------------------------------------------------------------------------------------
import yfinance as yf
import csv
import pandas as pd
import time

df=pd.read_csv('stock_id.csv', delimiter='\t')
historical_data = pd.DataFrame()
for i in df['證券代號']:
    stock_id=str(i)+".TW"
    data = yf.Ticker(stock_id)
    df = data.history(period="max")
    df['證券代號'] = i

    historical_data = pd.concat([historical_data, df])
    time.sleep(0.8)
    historical_data.to_csv('data.csv',encoding='utf-8-sig')
