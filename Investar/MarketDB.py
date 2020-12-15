import pandas as pd
import pymysql
from datetime import datetime

class MarketDB:
    def __init__(self):
        """생성자: MariaDB 연결 및 종목코드 딕셔너리 생성"""
        self.conn = pymysql.connect(host='localhost', user='root', password='dpfls', db='INVESTAR', charset='utf8')
        self.codes = dict()
        self.getCompanyInfo()
        
    def __del__(self):
        """소멸자: MariaDB 연결 해제"""
        self.conn.close()

    def getCompanyInfo(self):
        """company_info 테이블에서 읽어와서 companyData와 codes에 저장"""
        sql = "SELECT * FROM company_info"
        companyInfo = pd.read_sql(sql, self.conn)
        for idx in range(len(companyInfo)):
            self.codes[companyInfo['code'].values[idx]] = companyInfo['company'].values[idx]

    def getDailyPrice(self, code, startDate, endDate):
        """daily_price 테이블에서 읽어와서 데이터프레임으로 반환"""
        sql = "SELECT * FROM daily_price WHERE code = '{}' and date >= '{}' and date <= '{}'".format(code, startDate, endDate)
        df = pd.read_sql(sql, self.conn)
        df.index = df['date']
        return df
