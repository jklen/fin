# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 18:04:00 2021

@author: User
"""

#%% packages

import pickle
import yfinance as yf
import pandas as pd

#%% get finax etfs

finax_tickers_yf = ['FRCK.DE', 'XXSC.MI', 'XSX6.MI', 'XHYA.DE', 'XBLC.MI', 
					'DBZB.DE', 'IS3N.DE', 'ZPRR.DE', 'SPY4.DE', 'SXR8.DE']

df_finax = yf.download(tickers = ' '.join(finax_tickers_yf), period = 'max', interval = '1d')
pickle.dump(df_finax, open('data/df_finax.pickle', 'wb'))
#%% get all admiral etfs

df_admiral_etfs = pd.read_csv('materials/etf_list_admiral_markets.csv', sep = ';')
admiral_etfs_yf = df_admiral_etfs.loc[df_admiral_etfs['in yahoo fin'].isna(), 'yahoo ticker']
admiral_etfs_yf_list = admiral_etfs_yf.tolist()
df_admiral = yf.download(tickers = ' '.join(admiral_etfs_yf_list), period = 'max', interval = '1d')
pickle.dump(df_admiral, open('data/df_admiral_yf.pickle', 'wb'))
