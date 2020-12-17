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

df = df.assign(ema130=ema130, ema60=ema60, macd=macd, signal=signal,macdhist=macdhist).dropna()
df['number'] = df.index.map(mdates.date2num)
ohlc = df[['number','open','high','low','close']]

ndays_high = df.high.rolling(window=14, min_periods=1).max()      # 14일 동안의 최대값을 구한다.
ndays_low = df.low.rolling(window=14, min_periods=1).min()        # 14일 동안의 최소값을 구한다.
fast_k = (df.close - ndays_low) / (ndays_high - ndays_low) * 100  # 빠른 선 %K를 구한다.    
#??? : 공식은 +인데 왜 뺄까... (값을 더할 경우 80이상의 값만 출력됨..)
slow_d= fast_k.rolling(window=3).mean()                           # %K의 3일 동안의 평균을 구해 느린 선 %D를 구한다.
df = df.assign(fast_k=fast_k, slow_d=slow_d).dropna()             # %K와 %D로 데이터 프레임을 생성한 뒤 결측치는 제거한다.

plt.figure(figsize=(9, 7))
p1 = plt.subplot(2, 1, 1)
plt.title('Triple Screen Trading - Second Screen (NCSOFT)')
plt.grid(True)
candlestick_ohlc(p1, ohlc.values, width=.6, colorup='red', colordown='blue')
p1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.plot(df.number, df['ema130'], color='c', label='EMA130')
plt.legend(loc='best')

p1 = plt.subplot(2, 1, 2)
plt.grid(True)
p1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.plot(df.number, df['fast_k'], color='c', label='%K')
plt.plot(df.number, df['slow_d'], color='k', label='%D')
plt.yticks([10,20,80,100])
plt.legend(loc='best')
plt.show()