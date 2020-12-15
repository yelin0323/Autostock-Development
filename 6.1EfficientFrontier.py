#kospi의 상위 4종목의 랜덤한 보유 비율(포트폴리오)에 따른 리스크와 예상 수익률을 통한 효율적 투자선 분석 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Investar import Analyzer

mk = Analyzer.MarketDB()
stocks = ['삼성전자', 'SK하이닉스', '현대자동차', 'NAVER']
df = pd.DataFrame()
for s in stocks:
    df[s] = mk.get_daily_price(s, '2016-01-04', '2018-04-27')['close']
  
daily_ret = df.pct_change()     #시총 상위 4 종목의 일간 변동률을 구한다.
annual_ret = daily_ret.mean() * 252 #일간 변동률의 평균값에 252를 곱해서 연간 수익률을 구한다(252는 미국의 1년 평균 개장일)
daily_cov = daily_ret.cov()     #일간 리스크는 일간 변동률의 공분산으로 구한다
annual_cov = daily_cov * 252    #연간 공분산은 일간 공분산에 252를 곱해서 구한다.

port_ret = [] 
port_risk = [] 
port_weights = [] 

for _ in range(0, 20000): #포트폴리오 20,000개를 생성
    weights = np.random.random(len(stocks)) #4개의 랜덤 숫자로 구성된 배열을 생성
    weights /= np.sum(weights) #랜덤 숫자를 랜덤 숫자의 총 합으로 나눠 4 종목 비중의 합이 1이 되도록 조정

    returns = np.dot(weights, annual_ret) #종목별 비중 배열과 종목별 연간 수익률을 곱해 해당 포트폴리오 전체수익률을 구한다.
    risk = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights))) #해당 포트폴리오 전체 리스크를 구한다.

    port_ret.append(returns)     #포트폴리오 20,000개 수익률,
    port_risk.append(risk)       #리스크,
    port_weights.append(weights) #종목별 비중을 각각 리스트에 추가

portfolio = {'Returns': port_ret, 'Risk': port_risk} 
for i, s in enumerate(stocks): 
    portfolio[s] = [weight[i] for weight in port_weights] 
df = pd.DataFrame(portfolio) 
df = df[['Returns', 'Risk'] + [s for s in stocks]] 

df.plot.scatter(x='Risk', y='Returns', figsize=(8, 6), grid=True)
plt.title('Efficient Frontier') 
plt.xlabel('Risk')  #x축 : 해당 포트폴리오의 리스크
plt.ylabel('Expected Returns')  #y축 : 해당 포트폴리오의 예상 수익률
plt.show() 