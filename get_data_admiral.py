# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 18:50:06 2021

@author: User
"""

#%% import packages
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import MetaTrader5 as mt5
import pytz
import pickle

#%% connect to mt5
# connect to MetaTrader 5
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()
 
# request connection status and parameters
print(mt5.terminal_info())
# get data on MetaTrader 5 version
print(mt5.version())

#%% get admiral tickers
# time, open, high, low, close, tick_volume, spread, real_volume

df_adm_tickers = pd.read_csv('materials/etf_list_admiral_markets.csv')
adm_tickers = df_adm_tickers['INVESTsymbol'].tolist()

#%% get adm tickers from mt5
timezone = pytz.timezone("Etc/UTC")

utc_from = datetime(1990, 1, 1, tzinfo=timezone)
utc_to = datetime(2021, 3, 23, tzinfo=timezone)

dfs = pd.DataFrame()
for i, ticker in enumerate(adm_tickers):
	print(f'processing ticker - {i} - {ticker}...')
	try:
	
		rates = mt5.copy_rates_range(ticker, mt5.TIMEFRAME_D1, utc_from, utc_to)
		rates_frame = pd.DataFrame(rates)
		# convert time in seconds into the datetime format
		rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
		s = rates_frame['close']
		s.index = rates_frame['time']
		s.rename(ticker, inplace = True)
		dfs = dfs.join(s, how = 'outer')
	except Exception as e:
		print('!!!!something funny occured....getting data not successful!!!')
		print(e)

#%% save admiral df tickers
pickle.dump(dfs, open('data/df_admiral.pickle', 'wb'))
#%% shutdown mt5

mt5.shutdown()                    
