import pandas as pd
import matplotlib.pyplot as plt
import datetime
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
from Investar import Analyzer

mk = Analyzer.MarketDB()
df = mk.get_daily_price('엔씨소프트', '2017-01-01')


ema60 = df.close.ewm(span=60).mean()   # 종가의 12주(60일) 지수 이동평균
ema130 = df.close.ewm(span=130).mean() # 종가의 26주(130일) 지수 이동평균
macd = ema60 - ema130                  # MACD선
signal = macd.ewm(span=45).mean()      # MACD의 9주(45일) 지수 이동평균을 구해서 신호선으로 저장
macdhist = macd - signal               # MACD 히스토그램

df = df.assign(ema130=ema130, ema60=ema60, macd=macd, signal=signal,
    macdhist=macdhist).dropna() 
df['number'] = df.index.map(mdates.date2num)  # 캔들 차트 이용을 위해 날짜형 인덱스를 숫자형으로 변환
ohlc = df[['number','open','high','low','close']]

plt.figure(figsize=(9, 7))
p1 = plt.subplot(2, 1, 1)
plt.title('Triple Screen Trading - First Screen (NCSOFT)')
plt.grid(True)
candlestick_ohlc(p1, ohlc.values, width=.6, colorup='red', colordown='blue')  # OHLC 값을 이용하여 캔들차트를 그린다.
p1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.plot(df.number, df['ema130'], color='c', label='EMA130') #130일 이동평균선을 그린다.
plt.legend(loc='best')

p2 = plt.subplot(2, 1, 2)
plt.grid(True)
p2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.bar(df.number, df['macdhist'], color='m', label='MACD-Hist')
plt.plot(df.number, df['macd'], color='b', label='MACD')
plt.plot(df.number, df['signal'], 'g--', label='MACD-Signal')
plt.legend(loc='best')
plt.show()