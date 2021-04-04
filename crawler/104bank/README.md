import requests  
import json  
from bs4 import BeautifulSoup  
import csv  
import pandas as pd  
userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'  
headers ={'User-Agent':userAgent}  

ss = requests.session()  
data = [] #把取得的資訊都放入list  

for i in range(1,150): #自訂爬幾頁  
    url = f'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=python&order=12&asc=0&page={i}&mode=s'  
    res = ss.get(url,headers=headers)  
    soup = BeautifulSoup(res.text,'html.parser')  


    links = soup.select('a.js-job-link')  #取出這一頁所有職位的網址  

    for link in links:  
        link = link["href"].split("?")[0].split("/")[-1]  
       
        headers= {  
            'User-Agent': userAgent,  
            'Referer': f'https://www.104.com.tw/job/{link}?jobsource=jolist_b_relevance'}  
        
        res = f'https://www.104.com.tw/job/ajax/content/{link}'  
        res =ss.get(res,headers=headers)  #進入文章  
        jsonData = json.loads(res.text)  


        custName = jsonData['data']['header']['custName']  
        custUrl  =jsonData['data']['header']['custUrl']  
        jobName  =jsonData['data']['header']['jobName']  
        salary   =jsonData['data']['jobDetail']['salary']  
        jobDescription = jsonData['data']['jobDetail']['jobDescription']  
        otherDescription=jsonData['data']['condition']['other']  

        data.append([custName,custUrl,jobName,salary,jobDescription,otherDescription])  


columns=['公司名稱','網址','職缺名稱','薪資','職缺內容','其他條件']                     #第一欄的名稱  
df = pd.DataFrame(data=data, columns=columns)  
df.to_csv(r'./104_jobList.csv',index=False,encoding='utf-8-sig')  


#用pandas直接將csv存入  
import pandas as pd  
from sqlalchemy import create_engine  

# 初始化資料庫連線，使用pymysql模組  
engine = create_engine('mysql+pymysql://root:a9534068@localhost/stock?charset=utf8')  
# 讀取本地CSV檔案  
df = pd.read_csv("104_jobList.csv", sep=',')  
# 將新建的DataFrame儲存為MySQL中的資料表，不儲存index列  
df.to_sql('104', engine, index= False)  
print("Write to MySQL successfully!")  
