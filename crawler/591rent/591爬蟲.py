#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#存圖檔教學
import  requests
from bs4 import BeautifulSoup
import  os


folderName ='591house'
if not os.path.exists(folderName):
    os.mkdir(folderName)

userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
headers ={
    'User-Agent':userAgent
}
ss = requests.session()
url= 'https://rent.591.com.tw/?kind=0&region=1'

res =ss.get(url,headers=headers)
soup= BeautifulSoup(res.text,'html.parser')
links=soup.select('h3')
# print(links[15:30])

for link in links[0:15]:  #雖然一頁有30筆，但一次最多爬15筆，不然html太多會被洗掉
    link=link.select('a')[0]['href'].split("-")[2].split(".")[0]

    urlArticle =f"https://rent.591.com.tw/rent-detail-{link}.html"
    print(urlArticle)
    res = ss.get(url=urlArticle,headers=headers)
    soup =BeautifulSoup(res.text,'html.parser')
    print(soup)
    print(urlArticle)
    try:
        info = soup.select('div.houseIntro')[0].text
        title = soup.select('span.houseInfoTitle')[0].text
        price = soup.select('div.price.clearfix')[0].text
        lifebox = soup.select('div.lifeBox')[0].text
        # # pic =soup.select('textarea.datalazyload')[0]('img')[0]['src'].split('_')[0]
        pics = soup.select('textarea.datalazyload')[0]('img')
    except IndexError:
        pass

    for i,pic in enumerate(pics):
        picUrl = pic['src'].split('_')[0]+'_765x517.water3.jpg'
        resImg =requests.get(picUrl,headers=headers)
        imgContent = resImg.content
        try:
            with open(folderName + '/' + title + f'{i+1}.jpg', 'wb') as f:  # 寫入二進制
                f.write(imgContent)
        except FileNotFoundError:
            title = title.replace('/', '')
            with open(folderName + '/' + title + f'{i+1}.jpg', 'wb') as f:  # 寫入二進制
                f.write(imgContent)
        except OSError:
            title = title.replace('*', '')
            with open(folderName + '/' + title + f'{i+1}.jpg', 'wb') as f:  # 寫入二進制
                f.write(imgContent)


    try:
        with open(folderName + '/' + title + '.txt', 'a', encoding='utf-8') as f:
            f.write(title)
            f.write('\n')
            f.write(price)
            f.write('\n')
            f.write(lifebox)
            f.write('\n')
            f.write(info)
    except OSError:
        title= title.replace('*','')
        with open(folderName + '/' + title + '.txt', 'a', encoding='utf-8') as f:
            f.write(title)
            f.write('\n')
            f.write(price)
            f.write('\n')
            f.write(lifebox)
            f.write('\n')
            f.write(info)
    except FileNotFoundError:
        title = title.replace('/','')
        with open(folderName + '/' + title + '.txt', 'a', encoding='utf-8') as f:
            f.write(title)
            f.write('\n')
            f.write(price)
            f.write('\n')
            f.write(lifebox)
            f.write('\n')
            f.write(info)

