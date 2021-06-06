#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests 
import json 
import pandas as pd 
import dataframe_image as dfi

def Waterlevel():
    url='https://fhy.wra.gov.tw/fhy/api/ReservoirInfoApi/DryAreaGetAll'
    data=requests.get(url).text
    jsondata=json.loads(data)
    data=[]
    for product in jsondata:
        for i in product['DryView']:
            name=i['StationName']
            time=i['DATE']
            time=time.split("T")[0]
            over=i['Capacity']
            over=round(over)
            now=i['CapacityRate']
            now=round(now,2)
            data.append([name,time,over,now])
            
    columns = ['水庫名稱','更新日期','目前水量(m3)','目前百分比 %']
    df = pd.DataFrame(data=data, columns=columns) 
    dfi.export(df, 'dataframe.png')
    
if __name__ == '__main__':
    Waterlevel() 

