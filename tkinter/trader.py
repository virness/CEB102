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
from PIL import Image, ImageTk
import yfinance as yf
import talib as ta
def finance():
    keyword = b1.get()
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
    rate=f'均線   報酬率為:{rate}%'
    
    
    stk = yf.Ticker(f"{keyword}.TW")
    # 取得 2000 年至今的資料
    data = stk.history(start = '2016-01-01',end='2020-12-31')
    # 簡化資料，只取開、高、低、收以及成交量
    data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
    ret = data['Close'].pct_change()
    dif, dea, hist = ta.MACD(data['Close'])
    # 计算EMA12和EMA26
    ema12 = ta.EMA(data['Close'], 12)
    ema26 = ta.EMA(data['Close'], 26)
    sig2 = (hist>0) & (dea>0)
    sig2_lag = sig2.shift(1).fillna(0).astype(int)
    sig2_ret = sig2_lag*ret
    cum_sig2_ret = (1+sig2_ret).cumprod()
    cum_sig2_ret=cum_sig2_ret[-1:]
    cum_sig2_ret=np.array(cum_sig2_ret)
    cum_sig2_ret=cum_sig2_ret[0]*100
    cum_sig2_ret=round(cum_sig2_ret,2)
    cum_sig2_ret=f'MACD報酬率為:{cum_sig2_ret}%'
    
    
    stk = yf.Ticker(f'{keyword}.TW')
    # 取得 2000 年至今的資料
    data = stk.history(start = '2020-01-01',end='2020-12-31')
    # 簡化資料，只取開、高、低、收以及成交量
    data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
    Close=data.Close
    Open=data.Open
    def RSI(Close, period=14):
        # 整理資料
        Chg = Close - Close.shift(1)
        Chg_pos = pd.Series(index=Chg.index, data=Chg[Chg>0])
        Chg_pos = Chg_pos.fillna(0)
        Chg_neg = pd.Series(index=Chg.index, data=-Chg[Chg<0])
        Chg_neg = Chg_neg.fillna(0)
        up_mean = []
        down_mean = []
        for i in range(period+1, len(Chg_pos)+1):
            up_mean.append(np.mean(Chg_pos.values[i-period:i]))
            down_mean.append(np.mean(Chg_neg.values[i-period:i]))

        # 計算 RSI
        rsi = []
        for i in range(len(up_mean)):
            rsi.append( 100 * up_mean[i] / ( up_mean[i] + down_mean[i] ) )
        rsi_series = pd.Series(index = Close.index[period:], data = rsi)
        return rsi_series
    sig = []

    # 庫存標籤，只會是0或1，表示每次交易都是買進或賣出所有部位
    stock = 0
    RSI14 = RSI(Close, 14)
    # 偵測RSI14訊號
    for i in range(len(RSI14)):
        if RSI14[i] > 75 and stock == 1:
            stock -= 1
            sig.append(-1)
        elif RSI14[i] < 20 and stock == 0:
            stock += 1
            sig.append(1)
        else:
            sig.append(0)
    # 將訊號整理成dataframe
    rsi_sig = pd.Series(index = RSI14.index, data = sig)
    rets = []
    # 是否仍有庫存
    stock = 0
    # 當次交易買入價格
    buy_price = 0
    # 當次交易賣出價格
    sell_price = 0
    # 每次買賣的報酬率
    for i in range(len(rsi_sig)):
        if rsi_sig[i] == 1:
            # 隔日開盤買入
            buy_price = Open[rsi_sig.index[i+1]]
            stock += 1
        elif rsi_sig[i] == -1:
            # 隔日開盤賣出
            sell_price = Open[rsi_sig.index[i+1]]
            stock -= 1
            rets.append((sell_price-buy_price)/buy_price)
            # 清除上次買賣的價格
            buy_price = 0
            sell_price = 0
    # 總報酬率
    total_ret = 1
    for ret in rets:
        total_ret *= 1 + ret
    cum_ret=(str(round((total_ret - 1)*100,2)) + '%')  
    cum_ret=f'RSI    報酬率為{cum_ret}'
    
    
    t.insert('insert',rate)
    t.insert('insert','\n')
    t.insert('insert',cum_sig2_ret)
    t.insert('insert','\n')
    t.insert('insert',cum_ret)
    img = Image.open(f'./SMA/{keyword}.jpg')
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
L0 = tk.Label(win, text="CEB 102 大數據專題  技術分析 VS AI", font=("SimHei", 16))
L0.place(x=100, y=30)
# 單行文字
L1 = tk.Label(win, text="請輸入股票代號：", font=("SimHei", 16))
L1.place(x=75, y=60)

# 單行文字框  可採集鍵盤輸入
b1 = tk.Entry(win, font=("SimHei", 16), show=None, width=10)
b1.place(x=270, y=60)

# 設定查詢按鈕  點選 呼叫爬蟲函式實現查詢
a = tk.Button(win, text="查詢", width=5, height=1, command=finance)
a.place(x=420, y=60)

# 顯示結果的文字框
t = tk.Text(win, width=40, height=6, font=("SimHei", 18), selectforeground='red')  # 顯示多行文字
t.place(x=70, y=120)

# 進入訊息迴圈
win.mainloop()
