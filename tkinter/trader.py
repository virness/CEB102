#!/usr/bin/env python
# coding: utf-8

# In[44]:


import pandas as pd 
import numpy as np
import tkinter as tk
import datetime
import backtrader as bt
import backtrader.feeds as btfeeds
from datetime import datetime
import math
import matplotlib.pyplot as plot
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
def finance():
    keyword = b1.get()
    tradetype=comboExample.get()
    data = bt.feeds.YahooFinanceData(dataname='2330.TW',
                                 fromdate=datetime(2020, 1, 1),
                                 todate=datetime(2020, 12, 31))
    class SmaCross(bt.Strategy):
        # 交易紀錄
        def log(self, txt, dt=None):
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

        # 設定交易參數
        params = dict(
            ma_period_short=5,
            ma_period_long=20
        )

        def __init__(self):
            # 均線交叉策略
            sma1 = bt.ind.SMA(period=self.p.ma_period_short)
            sma2 = bt.ind.SMA(period=self.p.ma_period_long)
            self.crossover = bt.ind.CrossOver(sma1, sma2)

            # 使用自訂的sizer函數，將帳上的錢all-in
            self.setsizer(sizer())

            # 用開盤價做交易
            self.dataopen = self.datas[0].open

        def next(self):
            # 帳戶沒有部位
            if not self.position:
                # 5ma往上穿越20ma
                if self.crossover > 0:
                    # 印出買賣日期與價位
                    self.log('BUY ' + ', Price: ' + str(self.dataopen[0]))
                    # 使用開盤價買入標的
                    self.buy(price=self.dataopen[0])
    # 計算交易部位
    class sizer(bt.Sizer):
        def _getsizing(self, comminfo, cash, data, isbuy):
            if isbuy:
                return math.floor(cash/data[1])
            else:
                return self.broker.getposition(data)

    cerebro = bt.Cerebro()
    cerebro.addstrategy(SmaCross)
    cerebro.broker.setcash(10000)
    cerebro.adddata(data)
    cerebro.run()
    rate=float(cerebro.broker.getvalue()/10000)-1
    rate=rate*100
    rate=round(rate,2)
    rate=f'總報酬率為:{rate}%'
    t.insert('insert',rate)
    img = Image.open(f'./{tradetype}/{keyword}.jpg')
    img = img.resize((500, 400), Image.ANTIALIAS)
    imgTk =  ImageTk.PhotoImage(img)                        
    # 轉換成Tkinter可以用的圖片
    lbl_2 = tk.Label(win, image=imgTk)                   
    lbl_2.image = imgTk
    lbl_2.place(x = 20, y = 270)
win = tk.Tk()
# 設定視窗title和大小
win.title('交易回測')
win.geometry('550x700')

# 單行文字
L1 = tk.Label(win, text="請輸入股票代號：", font=("SimHei", 16))
L1.place(x=75, y=60)

# 單行文字框  可採集鍵盤輸入
b1 = tk.Entry(win, font=("SimHei", 16), show=None, width=10)
b1.place(x=240, y=60)

comboExample = ttk.Combobox(win, values=["SMA", "RSI","MACD","羅吉斯",'決策樹','Xgboost'],width=5,height=30,font=("SimHei", 16))
comboExample.grid(column=0, row=1,padx=350, pady=60)
comboExample.current(1)

# 設定查詢按鈕  點選 呼叫爬蟲函式實現查詢
a = tk.Button(win, text="查詢", width=5, height=1, command=finance)
a.place(x=430, y=60)

# 顯示結果的文字框
t = tk.Text(win, width=37, height=4, font=("SimHei", 18), selectforeground='red')  # 顯示多行文字
t.place(x=70, y=120)

# 進入訊息迴圈
win.mainloop()

