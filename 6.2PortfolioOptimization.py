import numpy as np
import numpy.random
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
sharpe_ratio = [] 

for _ in range(20000): 
    weights = np.random.random(len(stocks)) #4개의 랜덤 숫자로 구성된 배열을 생성
    weights /= np.sum(weights) #랜덤 숫자를 랜덤 숫자의 총 합으로 나눠 4 종목 비중의 합이 1이 되도록 조정

    returns = np.dot(weights, annual_ret) #종목별 비중 배열과 종목별 연간 수익률을 곱해 해당 포트폴리오 전체수익률을 구한다.
    risk = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights))) #해당 포트폴리오 전체 리스크를 구한다.

    port_ret.append(returns)     #포트폴리오 20,000개 수익률,
    port_risk.append(risk)       #리스크,
    port_weights.append(weights) #종목별 비중을 각각 리스트에 추가

    sharpe_ratio.append(returns/risk)  # 샤프 지수 리스트에 추가 (샤프 지수 = (예상 수익률-무위험률)/수익률의 표준편차)

portfolio = {'Returns': port_ret, 'Risk': port_risk, 'Sharpe': sharpe_ratio}

for i, s in enumerate(stocks): 
    portfolio[s] = [weight[i] for weight in port_weights] 
df = pd.DataFrame(portfolio) 
df = df[['Returns', 'Risk', 'Sharpe'] + [s for s in stocks]]  # 샤프 지수 칼럼을 데이터 프레임에 추가

max_sharpe = df.loc[df['Sharpe'] == df['Sharpe'].max()]  # 샤프 지숫값이 제일 큰 행을 max_sharpe로 정함
min_risk = df.loc[df['Risk'] == df['Risk'].min()]  # 리스크 칼럼에서 리스크값이 제일 작은 행을 min_risk로 정함

df.plot.scatter(x='Risk', y='Returns', c='Sharpe', cmap='viridis',
    edgecolors='k', figsize=(11,7), grid=True)  # 컬러맵을 'viridis'로 표시하고 테두리는 검정으로 표시
plt.scatter(x=max_sharpe['Risk'], y=max_sharpe['Returns'], c='r', 
    marker='*', s=300)  # 샤프지수가 가장 큰 포트폴리오를 300크기의 붉은 별로 표시
plt.scatter(x=min_risk['Risk'], y=min_risk['Returns'], c='r', 
    marker='X', s=200)  # 리스크가 제일 작은 포트폴리오를 200 크기의 붉은 x표로 표시
plt.title('Portfolio Optimization') 
plt.xlabel('Risk') 
plt.ylabel('Expected Returns') 
plt.show()