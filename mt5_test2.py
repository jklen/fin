# -*- coding: utf-8 -*-
"""
Created on Sat May 30 19:25:43 2020

@author: User
"""

from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import MetaTrader5 as mt5
from datetime import datetime
import pytz

# https://www.mql5.com/en/docs/integration/python_metatrader5/mt5symbolsget_py
 
# connect to MetaTrader 5
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()
 
# request connection status and parameters
print(mt5.terminal_info())
print('--------------')
# get data on MetaTrade

# login to my account and print account info
account=1111
server = 'AdmiralMarkets-Live'
password = 'password'
authorized=mt5.login(login = account,server = server, password=password)
if authorized:
	# display trading account data in the form of a list
	print("Show account_info()._asdict():")
	account_info_dict = mt5.account_info()._asdict()
	for prop in account_info_dict:
		print("  {}={}".format(prop, account_info_dict[prop]))
else:
	print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))

# get number of all financial instruments in the terminal
symbols_nr = mt5.symbols_total()
print(f'total symbols {symbols_nr}')

# get selected symbols current info
my_symbols_etf = ['IVE', 'VWRL', 'IVW', 'SWDA', 'IMEA', 'IJH', 'IWM', 'VLUE', 'SPY', 'ITOT', 'ITB',
				'IJR', 'XLK', 'QQQ', 'IXJ', 'XBI', 'IBB', 'UBIO', 'IAU', 'SLV',
				'XLRE', 'IEI', 'TLTUS', 'MSCI', 'SDIV', 'HDV', 'VYM', 'SPHD']
my_symbols_stocks = ['MSFT', 'ORCL', 'NVDA', 'INTC','GOOG', 'AMD', 'ZOOM', 'DELL', 'AAPL', 'SYNA', 'DPZ', 'CROX', 'AMZN', 'BRKB',
					 'HSBA', 'BNP', 'DBK', 'BLK', 'BABA', 'SPOT', 'PYPL', 'NFLX', 'STOR', 'SAFE', 'SP', 'RIO','GAZ',
					 'CVX', 'BP', 'ROSN', 'D', 'ES', '7272.JP', 'BAYN', 'TSLA', 'ABT', 'UCB',
					 'MRNA', 'GILD', 'BSX', 'REGN', 'VRTX', 'LUV', 'BCO', 'DAL']
my_sybols_etf_fed = ['VCIT', 'HYG' ,'VCSH', 'JNK', 'IGIB', 'LQD', 'SPIB', 'IGSB', 'ANGL']
my_symbols_etf_info = {}

for symbol in my_symbols_etf:
	symbol_info_dict = mt5.symbol_info(symbol)._asdict()
	my_symbols_etf_info[symbol] = symbol_info_dict
	
# get info about symbols last tick

my_symbols_etf_last_ticks = {}
for symbol in my_symbols_etf:
	symbol_last_tick_dict = mt5.symbol_info_tick(symbol)._asdict()
	my_symbols_etf_last_ticks[symbol] = symbol_last_tick_dict
	

# include or exclude a symbol from the marketwatch window
selected=mt5.symbol_select("GBPUSD",True)
selected=mt5.symbol_select("GBPUSD",False)

for symbol in my_symbols_etf:
	selected=mt5.symbol_select(symbol,True)
	
for symbol in my_symbols_stocks:
	selected=mt5.symbol_select(symbol,True)
	
for symbol in my_sybols_etf_fed:
	selected=mt5.symbol_select(symbol,True)

# get rates - time, open, high, low, close, tick_volume, spread and real_volume columns
my_symbols_etf_rates = {}
for symbol in my_symbols_etf:
	symbol_rates = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_D1, datetime(2020,5, 22, 23), 10) # 10 trading days back from 22.5.2020
	df_symbol_rates = pd.DataFrame(symbol_rates)
	df_symbol_rates['time'] = pd.to_datetime(df_symbol_rates['time'], unit='s')
	my_symbols_etf_rates[symbol] = df_symbol_rates

# get rates - time, open, high, low, close, tick_volume, spread and real_volume columns - position based
my_symbols_etf_rates = {}
for symbol in my_symbols_etf:
	symbol_rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_D1, 0, 10) # 10 trading days back from today
	df_symbol_rates = pd.DataFrame(symbol_rates)
	df_symbol_rates['time'] = pd.to_datetime(df_symbol_rates['time'], unit='s')
	my_symbols_etf_rates[symbol] = df_symbol_rates

# get rates - time, open, high, low, close, tick_volume, spread and real_volume columns - range based
my_symbols_etf_rates = {}
for symbol in my_symbols_etf:
	symbol_rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_D1, datetime(2020,5, 18), datetime(2020,5, 22, 23)) 
	df_symbol_rates = pd.DataFrame(symbol_rates)
	df_symbol_rates['time'] = pd.to_datetime(df_symbol_rates['time'], unit='s')
	my_symbols_etf_rates[symbol] = df_symbol_rates

# get ticks from - what are TICKS and how this data can be used?
my_symbols_etf_ticks = {}
for symbol in my_symbols_etf:
	symbol_ticks = mt5.copy_ticks_from(symbol, datetime(2020,5, 18, 0), 100, mt5.COPY_TICKS_TRADE) 
	df_symbol_ticks = pd.DataFrame(symbol_ticks)
	df_symbol_ticks['time'] = pd.to_datetime(df_symbol_ticks['time'], unit='s')
	my_symbols_etf_ticks[symbol] = df_symbol_ticks

# copy ticks range function
timezone = pytz.timezone("Etc/UTC")
my_symbols_etf_ticks = {}
for symbol in my_symbols_etf:
	symbol_ticks = mt5.copy_ticks_range(symbol, datetime(2020,7,14,0,  tzinfo=timezone), datetime(2020, 7,17,23,  tzinfo=timezone), mt5.COPY_TICKS_ALL)
	df_symbol_ticks = pd.DataFrame(symbol_ticks)
	df_symbol_ticks['time'] = pd.to_datetime(df_symbol_ticks['time'], unit='s')
	my_symbols_etf_ticks[symbol] = df_symbol_ticks

# get total number of active orders
orders = mt5.orders_total()

# get total number of open positions
positions = mt5.positions_total()





mt5.shutdown()