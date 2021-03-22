# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 16:04:38 2021

@author: Jaroslav_Klen
"""
#%%
import time
finax_tickers = ['FRCK', 'XXSC', 'XSX6', 'XHYA', 'XBLC', 'DBZB', 'IS3N', 'ZPRR', 'SPY4', 'SXR8']

#%%

from alpha_vantage.timeseries import TimeSeries

ts = TimeSeries(key='F5DIRSGL3KXINNCM', output_format = 'pandas')
# Get json object with the intraday data and another with  the call's metadata
#data, meta_data = ts.get_intraday('SPY')

dfs = []
metas = []
for ticker in finax_tickers:
    try:
        df, meta = ts.get_monthly(ticker)
        dfs.append(df)
        metas.append(meta)
    except Exception as e:
        print(f'ticker {ticker} data retreive error...')
        print(e)
    else:
        print(f'ticker {ticker} SUCCESS.....')
    time.sleep(13)
    
#%%

import investpy
# https://investpy.readthedocs.io/_info/introduction.html

# Retrieve all the available stocks as a Python list
stocks = investpy.get_stocks_list()
funds = investpy.get_funds_list()
etfs = investpy.get_etfs_list()

# Retrieve the recent historical data (past month) of a stock as a pandas.DataFrame on ascending date order
df_bbva = investpy.get_stock_recent_data(stock='bbva', country='spain', as_json=False, order='ascending')

# Retrieve the company profile of the introduced stock on english
profile = investpy.get_stock_company_profile(stock='bbva', country='spain', language='english')

df_aapl = investpy.get_stock_historical_data(stock='AAPL',
                                        country='United States',
                                        from_date='01/01/2010',
                                        to_date='01/01/2020')

df_fund = investpy.get_fund_historical_data(fund='bbva plan multiactivo moderado pp',
                                       country='spain',
                                       from_date='01/01/2010',
                                       to_date='01/01/2019')

df_bbva_etf = investpy.get_etf_recent_data(etf='bbva accion dj eurostoxx 50',
                                  country='spain')
etfs_ger = investpy.get_etfs_list(country = 'germany')

investpy.get_stock_countries()

#%% get finax tickers
from_date = '01/01/1990'
to_date = '21/03/2021'

search = investpy.search_quotes('FRCK')
df_frck = search[0].retrieve_historical_data(from_date=from_date, to_date=to_date)
#df_frck.columns = 'frck_' + df_frck.columns

search = investpy.search_quotes('XXSC')
df_xxsc = search[0].retrieve_historical_data(from_date=from_date, to_date=to_date) # etf - xetra
#df_xxsc.columns = 'xxsc_' + df_xxsc.columns

search = investpy.search_quotes('XSX6')
df_xsx6 = search[1].retrieve_historical_data(from_date=from_date, to_date=to_date)
#df_xsx6.columns = 'xsx6_' + df_xsx6.columns

search = investpy.search_quotes('XHYA')
df_xhya = search[0].retrieve_historical_data(from_date=from_date, to_date=to_date)
#df_xhya.columns = 'xhya_' + df_xhya.columns

search = investpy.search_quotes('XBLC') 
df_xblc = search[0].retrieve_historical_data(from_date=from_date, to_date=to_date)
#df_xblc.columns = 'xblc_' + df_xblc.columns

# DBZB - vyzera rovnako ako XGSH
# len ina burza https://www.trackinsight.com/en/fund/LU0378818131

search = investpy.search_quotes('XGSH') 
df_xgsh = search[0].retrieve_historical_data(from_date=from_date, to_date=to_date)
#df_xgsh.columns = 'xgsh_' + df_xgsh.columns

search = investpy.search_quotes('IS3N') 
df_is3n = search[0].retrieve_historical_data(from_date=from_date, to_date=to_date)


search = investpy.search_quotes('ZPRR') 
df_zprr = search[0].retrieve_historical_data(from_date=from_date, to_date=to_date)

search = investpy.search_quotes('SPY4') 
df_spy4 = search[3].retrieve_historical_data(from_date=from_date, to_date=to_date)

search = investpy.search_quotes('SXR8') 
df_sxr8 = search[0].retrieve_historical_data(from_date=from_date, to_date=to_date)