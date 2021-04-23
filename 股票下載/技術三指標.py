#!/usr/bin/env python
# coding: utf-8

# In[35]:


import yfinance as yf
import pandas as pd 
import numpy as np
df=[2330,2317,2454,2308,2303,3711,3008,2382,3034,3045,2357,2327,2395,2379,8046,6415,4904,3481,2409,4938,2474,2345,2301,6669,2377,3037,2492,2324,2344,4958,5269,2354,2356,6409,2353,2347,6239,3702,2360,3044,2352,2376,2458,2383,3406,3532,3533
,1101,2002,2886]
for j in df:
    stk = yf.Ticker(str(j)+'.TW')
        # 取得 2000 年至今的資料
    data = stk.history(start = '2020-01-01',end='2020-12-31')
        # 簡化資料，只取開、高、低、收以及成交量
    data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
    Close=data['Close']
    def RSI(Close, period=14):
            # 整理資料
        Chg = Close - Close.shift(1)
        Chg_pos = pd.Series(index=Chg.index, data=Chg[Chg>0])
        Chg_pos = Chg_pos.fillna(0)
        Chg_neg = pd.Series(index=Chg.index, data=-Chg[Chg<0])
        Chg_neg = Chg_neg.fillna(0)
            # 計算平均漲跌幅度
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
    RSI14_2020 = RSI(Close, 14)
        # 庫存標籤，只會是0或1，表示每次交易都是買進或賣出所有部位
    stock = 0

        # 偵測RSI14訊號
    for i in range(len(RSI14_2020)):
        if RSI14_2020[i] > 80 and stock == 1:
            stock -= 1
            sig.append(-1)
        elif RSI14_2020[i] < 30 and stock == 0:
            stock += 1
            sig.append(1)
        else:
            sig.append(0)
        # 將訊號整理成dataframe
    rsi_sig = pd.Series(index = RSI14_2020.index, data = sig)
    Open2020 = data['Open']

        # 每次買賣的報酬率
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
            buy_price = Open2020[rsi_sig.index[i+1]]
            stock += 1
        elif rsi_sig[i] == -1:
                # 隔日開盤賣出
            sell_price = Open2020[rsi_sig.index[i+1]]
            stock -= 1
            rets=((sell_price-buy_price)/buy_price)
                # 清除上次買賣的價格
            buy_price = 0
            sell_price = 0    
            rate = (1 + rets).cumprod()-1
    
            print(j)
            print(rate)
            print('----------------')


# In[36]:


import yfinance as yf
import talib as ta
import pandas as pd
df=[2330,2317,2454,2308,2303,3711,3008,2382,3034,3045,2357,2327,2395,2379,8046,6415,4904,3481,2409,4938,2474,2345,2301,6669,2377,3037,2492,2324,2344,4958,5269,2354,2356,6409,2353,2347,6239,3702,2360,3044,2352,2376,2458,2383,3406,3532,3533
,1101,2002,2886]
for j in df:
    stk = yf.Ticker(str(j)+".TW")
    # 取得 2000 年至今的資料
    data = stk.history(start = '2016-01-01',end='2020-12-31')
    # 簡化資料，只取開、高、低、收以及成交量
    data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
    ret = data['Close'].pct_change()
    dif, dea, hist = ta.MACD(data['Close'])
    # 计算EMA12和EMA26
    ema12 = ta.EMA(data['Close'], 12)
    ema26 = ta.EMA(data['Close'], 26)

    # sig1只考虑HIST指标，HIST转正时开仓买入，转负时清仓
    sig1 = (hist>0)
    # sig2同时考虑HIST指标和DEA指标，只有当HIST转正，且DEA在0以上时，才开仓买入，任何一个指标变负即清仓。
    # 这是文献中建议的方法
    sig2 = (hist>0) & (dea>0)
    # sig3同时考虑HIST和EMA指标，只有当HIST为正，而且当前价格在慢线（26日指数加权平均价）上方时，才开仓买入，任何一个指标转负即清仓。
    # 网上有人建议过这种方法（如果我没有理解错的话）
    sig3 = (hist>0) & (data['Close']>ema26)

    sig2_lag = sig2.shift(1).fillna(0).astype(int)
    # sig2_lag与股票日收益率相乘，即可得策略日收益率。python能自动对齐时间序列的日期。
    sig2_ret = sig2_lag*ret
    # 计算策略累计收益
    cum_sig2_ret = (1+sig2_ret).cumprod()
    cum_sig2_ret=cum_sig2_ret[-1:]
    print(j,cum_sig2_ret)


# In[37]:


import yfinance as yf
import pandas as pd 
import talib as ta
df=[2330,2317,2454,2308,2303,3711,3008,2382,3034,3045,2357,2327,2395,2379,8046,6415,4904,3481,2409,4938,2474,2345,2301,6669,2377,3037,2492,2324,2344,4958,5269,2354,2356,6409,2353,2347,6239,3702,2360,3044,2352,2376,2458,2383,3406,3532,3533
,1101,2002,2886]
for j in [df]:
    stk = yf.Ticker(str(j)+'.TW')
        # 取得 2000 年至今的資料
    data = stk.history(start = '2016-01-01',end='2020-12-31')
        # 簡化資料，只取開、高、低、收以及成交量
    data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
#     ret = data['Close'].pct_change()
    Open=data['Open']
    Close=data['Close']
    ma5 =ta.SMA(Close, 5)
    ma20=ta.SMA(Close,20)
    # 5ma與20ma差距
    MA_dif = ma5 - ma20

    # 參數
    stock = 0
    sig = [] 

    # 訊號
    for i in range(len(MA_dif)):
        # 5MA往上穿越10MA
#         if MA_dif[i-1] < 0 and MA_dif[i] > 0 and stock == 0:
        if MA_dif[i] > 0 and stock == 0:
            stock += 1
            sig.append(1)

        # 5MA往下穿越10MA
#         elif MA_dif[i-1] > 0 and MA_dif[i] < 0 and stock == 1:
        elif MA_dif[i] < 0 and stock == 1:
            stock -= 1
            sig.append(-1)
        else:
            sig.append(0)
    ma_sig = pd.Series(index = MA_dif.index, data = sig)
    rets = []
    transaction = []

    # 是否仍有庫存
    stock = 0
    stock_his = []

    # 當次交易買入價格
    buy_price = 0

    # 當次交易賣出價格
    sell_price = 0

    # 每次買賣的報酬率
    for i in range(len(ma_sig)-1):
        stock_his.append(stock)
        if ma_sig[i] == 1:
            # 隔日開盤買入
            buy_price = Open[ma_sig.index[i+1]]
            stock += 1
            # 紀錄交易日期
            transaction.append([ma_sig.index[i+1],'buy'])
        elif ma_sig[i] == -1:
            # 隔日開盤賣出
            sell_price = Open[ma_sig.index[i+1]]
            stock -= 1
            rets.append((sell_price-buy_price)/buy_price)
            # 賣出後就清空資料
            buy_price = 0
            sell_price = 0
            # 紀錄交易日期
            transaction.append([ma_sig.index[i+1],'sell'])

    # 如果最後手上有庫存，就用回測區間最後一天的開盤價賣掉
    if stock == 1 and buy_price != 0 and sell_price == 0:
        sell_price = Open[-1]
        rets.append((sell_price-buy_price)/buy_price)
        stock -= 1
        transaction.append([Open.index[-1],'sell'])
    total_ret = 1
    for ret in rets:
        total_ret *= (1 + ret)
    print(j)
    print('總報酬率：' + str(round(100*(total_ret-1),2)) + '%')
    print('----------')

