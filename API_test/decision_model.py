# -*- coding: utf-8 -*-
"""crypto_prediction 2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gaNt7wc7lx34kKmACbU5lmrDuBel4Lx4
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import datetime as dt 
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense ,Dropout, LSTM
from tensorflow.keras.models import Sequential
#!pip install yfinance
import yfinance as yf
from datetime import datetime



# ___library_import_statements___
import pandas as pd

# for pandas_datareader, otherwise it might have issues, sometimes there is some version mismatch
pd.core.common.is_list_like = pd.api.types.is_list_like

# make pandas to print dataframes nicely
pd.set_option('expand_frame_repr', False)  


#import pandas_datareader.data as web
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time

# ___variables___
ticker = 'AAPL'

start_time = datetime.datetime(2017, 10, 1)
#end_time = datetime.datetime(2019, 1, 20)
end_time = datetime.datetime.now().date().isoformat()       

start = dt.datetime(2020,1,1) 
end = dt.datetime.now()
Crypto_currency = "BTC"
Real_currency = "USD"

BTC_USD = yf.Ticker(f"{Crypto_currency}-{Real_currency}")
ticker_df = BTC_USD.history(start=start, end=end) 
ticker_df = ticker_df.reset_index()

df = ticker_df


def computeRSI (data, time_window):
    diff = data.diff(1).dropna()        # diff in one field(one day)

    #this preservers dimensions off diff values
    up_chg = 0 * diff
    down_chg = 0 * diff
    
    # up change is equal to the positive difference, otherwise equal to zero
    up_chg[diff > 0] = diff[ diff>0 ]
    
    # down change is equal to negative deifference, otherwise equal to zero
    down_chg[diff < 0] = diff[ diff < 0 ]
    
    # check pandas documentation for ewm
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
    # values are related to exponential decay
    # we set com=time_window-1 so we get decay alpha=1/time_window
    up_chg_avg   = up_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    
    rs = abs(up_chg_avg/down_chg_avg)
    rsi = 100 - 100/(1+rs)
    return rsi

df['RSI'] = computeRSI(df['Close'], 14)
df["decision"] = df.RSI
df.decision.fillna(0, inplace = True)
df.RSI.fillna(0, inplace = True)

df.decision[df.RSI >= 70] = "sell"
df.decision[df.RSI <= 30] = "invest"
df.decision[(df.RSI < 70)  & (df.RSI > 30)] = "hold"

def print_dict():
    dict = {}
    for i in np.arange(df.Date.size):
        dict[str(df.Date[i])] = df.decision[i]
    return dict 

print(print_dict())
#date_time_obj = datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S') 