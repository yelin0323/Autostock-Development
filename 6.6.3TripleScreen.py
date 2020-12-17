#주간 추세가 상승하고 있을 떄, 일간 오실레이터가 하락하면서 매수 신호가 발생하면
#전일 고점보다 한 틱 위에서 매수준을 낸다 -> 추적 매수 스톱
#130일 이동 지수평균이 상승하고 %D가 20 아래로 떨어질 때 매수
#130일 이동 지수평균이 하락하고 %D가 80 위로 올라갈 때 매도

import pandas as pd
import matplotlib.pyplot as plt
import datetime
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
from Investar import Analyzer

mk = Analyzer.MarketDB()
df = mk.get_daily_price('엔씨소프트', '2019-01-01')

ema60 = df.close.ewm(span=60).mean()   # 종가의 12주(60일) 지수 이동평균
ema130 = df.close.ewm(span=130).mean() # 종가의 26주(130일) 지수 이동평균
macd = ema60 - ema130                  # MACD선
signal = macd.ewm(span=45).mean()      # MACD의 9주(45일) 지수 이동평균을 구해서 신호선으로 저장
macdhist = macd - signal               # MACD 히스토그램
df = df.assign(ema130=ema130, ema60=ema60, macd=macd, signal=signal, macdhist=macdhist).dropna()

df['number'] = df.index.map(mdates.date2num)
ohlc = df[['number','open','high','low','close']]

ndays_high = df.high.rolling(window=14, min_periods=1).max()      # 14일 동안의 최대값을 구한다.
ndays_low = df.low.rolling(window=14, min_periods=1).min()        # 14일 동안의 최소값을 구한다.

fast_k = (df.close - ndays_low) / (ndays_high - ndays_low) * 100  # 빠른 선 %K를 구한다.    
slow_d= fast_k.rolling(window=3).mean()                           # %K의 3일 동안의 평균을 구해 느린 선 %D를 구한다.
df = df.assign(fast_k=fast_k, slow_d=slow_d).dropna()  

plt.figure(figsize=(9, 9))
p1 = plt.subplot(3, 1, 1)
plt.title('Triple Screen Trading (NCSOFT)')
plt.grid(True)
candlestick_ohlc(p1, ohlc.values, width=.6, colorup='red', colordown='blue')
p1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.plot(df.number, df['ema130'], color='c', label='EMA130')
for i in range(1, len(df.close)):
    if df.ema130.values[i-1] < df.ema130.values[i] and df.slow_d.values[i-1] >= 20 and df.slow_d.values[i] < 20:
        plt.plot(df.number.values[i], 250000, 'r^')     #130일 이동 지수평균이 상승하고 %D가 20 아래로 떨어질 때 매수
    elif df.ema130.values[i-1] > df.ema130.values[i] and df.slow_d.values[i-1] <= 80 and df.slow_d.values[i] > 80:
        plt.plot(df.number.values[i], 250000, 'bv')     #130일 이동 지수평균이 하락하고 %D가 80 위로 올라갈 때 매도
plt.legend(loc='best')

p2 = plt.subplot(3, 1, 2)
plt.grid(True)
p2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.bar(df.number, df['macdhist'], color='m', label='MACD-Hist')
plt.plot(df.number, df['macd'], color='b', label='MACD')
plt.plot(df.number, df['signal'], 'g--', label='MACD-Signal')
plt.legend(loc='best')

p3 = plt.subplot(3, 1, 3)
plt.grid(True)
p3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.plot(df.number, df['fast_k'], color='c', label='%K')
plt.plot(df.number, df['slow_d'], color='k', label='%D')
plt.yticks([0, 20, 80, 100])
plt.legend(loc='best')
plt.show()