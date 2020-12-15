import matplotlib.pyplot as plt
from Investar import Analyzer

mk = Analyzer.MarketDB()
df = mk.get_daily_price('NAVER', '2019-01-02')
  
df['MA20'] = df['close'].rolling(window=20).mean()  # 20개 종가를 이용해서 평균을 구한다.
df['stddev'] = df['close'].rolling(window=20).std() # 20개 종가를 이용해서 표준편차를 구한 뒤 stddev 칼럼으로 df에 추가한다.
df['upper'] = df['MA20'] + (df['stddev'] * 2)   # 상단 볼린저 밴드 게산
df['lower'] = df['MA20'] - (df['stddev'] * 2)   # 하단 볼린저 밴드 계산
df['PB'] = (df['close'] - df['lower']) / (df['upper'] - df['lower']) #(종가-하단밴드) / (상단밴드-하단밴드)를 구해 %B 칼럼을 생성
df['bandwidth'] = (df['upper']-df['lower'])/df['MA20']*100 #(상단 밴드 - 하단 밴드) / 중간 밴드 x 100을 구해 bandwidth(밴드 폭) 칼럼을 생성
df = df[19:]  

plt.figure(figsize=(9, 12))
plt.subplot(3,1,1)
plt.plot(df.index, df['close'], color='#0000ff', label='Close')    # x좌표 df.index에 해당하는 종가를 y좌표로 설정해 파란색 실선으로 표시
plt.plot(df.index, df['upper'], 'r--', label = 'Upper band')       # x좌표 df.index에 해당하는 상단 볼린저 밴드값을 y좌표로 설정해 검은실선으로 표시
plt.plot(df.index, df['MA20'], 'k--', label='Moving average 20')
plt.plot(df.index, df['lower'], 'c--', label = 'Lower band')       #하단 볼린저 밴드값을 시안색 실선으로 표시
plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')  #상단 볼린저 밴드와 하단 볼린저 밴드 사이를 회색으로 칠한다.
plt.legend(loc='best')
plt.title('NAVER Bollinger Band (20 day, 2 std)')
plt.legend(loc='best')

plt.subplot(3, 1, 2)  
plt.plot(df.index, df['PB'], color='b', label='%B')  #x 좌표 df.index에 해당하는 %b값을 y좌표로 설정해 파란(b) 실선으로 표시
plt.grid(True)
plt.legend(loc='best')

#급락,급상승 할 때 bandwidth가 증가한다.
plt.subplot(3, 1, 3)
plt.plot(df.index, df['bandwidth'], color = 'm', label = 'Bandwidth')
plt.grid(True)
plt.legend(loc = 'best')
plt.show() 