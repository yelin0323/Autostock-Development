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

df['TP'] = (df['high'] + df['low'] + df['close']) / 3 #고가,저가,종가의 합을 3으로 나눠서 중심가격 TP를 구한다.
df['PMF'] = 0
df['NMF'] = 0
for i in range(len(df.close)-1):    #0부터 -2까지 반복
    if df.TP.values[i] < df.TP.values[i+1]: 
        df.PMF.values[i+1] = df.TP.values[i+1] * df.volume.values[i+1] #긍정적 현금 흐름(PMF)에 저장
        df.NMF.values[i+1] = 0
    else:
        df.NMF.values[i+1] = df.TP.values[i+1] * df.volume.values[i+1]  #부정적 현금 흐름(NMF)에 저장
        df.PMF.values[i+1] = 0
df['MFR'] = (df.PMF.rolling(window=10).sum() /
    df.NMF.rolling(window=10).sum())        #현금 흐름 비율(MFR = PMF/NMF)
df['MFI10'] = 100 - 100 / (1 + df['MFR']) #10일 기준으로 현금흐름지수를 계산한 결과를 MFI10 칼럼에 저장
df = df[19:]

plt.figure(figsize=(9, 8))
plt.subplot(2,1,1)
plt.plot(df.index, df['close'], color='#0000ff', label='Close')    # x좌표 df.index에 해당하는 종가를 y좌표로 설정해 파란색 실선으로 표시
plt.plot(df.index, df['upper'], 'r--', label = 'Upper band')       # x좌표 df.index에 해당하는 상단 볼린저 밴드값을 y좌표로 설정해 검은실선으로 표시
plt.plot(df.index, df['MA20'], 'k--', label='Moving average 20')
plt.plot(df.index, df['lower'], 'c--', label = 'Lower band')       #하단 볼린저 밴드값을 시안색 실선으로 표시
plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')  #상단 볼린저 밴드와 하단 볼린저 밴드 사이를 회색으로 칠한다.
for i in range(len(df.close)):
    if df.PB.values[i] > 0.8 and df.MFI10.values[i] > 80:       # %B가 0.8보다 크고 10일 기준 MFI가 80보다 크면
        plt.plot(df.index.values[i], df.close.values[i], 'r^')  # 매수 시점을 나타내기 위해 첫 번째 그래프의 종가 위치에 빨간색 삼각형을 표시
    elif df.PB.values[i] < 0.2 and df.MFI10.values[i] < 20:     # %b가 0.2보다 작고 10일 기준 MFI가 20보다 작으면
        plt.plot(df.index.values[i], df.close.values[i], 'bv')  # 매도 시점을 나타내기 위해 첫 번째 그래프의 종가 위치에 파란색 삼각형을 표시
plt.legend(loc='best')
plt.title('NAVER Bollinger Band (20 day, 2 std)')

plt.subplot(2, 1, 2)
plt.plot(df.index, df['PB'] * 100, 'b', label='%B x 100')       # MFI와 비교할 수 있게 %b를 그대로 표시하지 않고 100을 곱해서 푸른색 실선으로 표시
plt.plot(df.index, df['MFI10'], 'g--', label='MFI(10 day)')     # 10일 기준 MFI를 녹색의 점선으로 표시
plt.yticks([-20, 0, 20, 40, 60, 80, 100, 120])                  # y축 눈금을 -20qnxj 120까지 20 단위로 표시
for i in range(len(df.close)):
    if df.PB.values[i] > 0.8 and df.MFI10.values[i] > 80:
        plt.plot(df.index.values[i], 0, 'r^')
    elif df.PB.values[i] < 0.2 and df.MFI10.values[i] < 20:
        plt.plot(df.index.values[i], 0, 'bv')
plt.grid(True)
plt.legend(loc='best')
plt.show()