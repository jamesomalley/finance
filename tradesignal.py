# -*- coding: utf-8 -*-
"""
References used:
https://codingandfun.com/scrape-yahoo-finance-using-python/
https://algotrading101.com/learn/robinhood-api-guide/
https://robin-stocks.readthedocs.io/
http://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
https://medium.com/swlh/parabolic-stop-and-reverse-indicator-the-full-guide-d4c7193ca53d
https://alexanderle.com/send-sms-python#:~:text=How%20To%20Send%20A%20SMS%20Message%20With%20Python,send%20e-mail.%20...%204%20Send%20The%20Message.%20

"""
#Load Libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go


import robin_stocks.robinhood as rs
import pyotp
import smtplib

import numpy as np
import talib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt

# Authentications
totp  = pyotp.TOTP("My2factorAppHere").now()
#print("Current OTP:", totp)

rs.authentication.login(username=XXXXXX,
         password=XXXXXXX,
         expiresIn=86400,
         by_sms=True,
         mfa_code=totp)

server = smtplib.SMTP( "smtp.gmail.com", 587 )
server.starttls()
server.login( XXXXXXX, XXXXXXXX )

#Setup Dash


#Load Data
ticker= 'GE'

if ticker in ['BTC','ETH','DOGE','BSV','LTC','BCH','ETC']:
        print("It's Crypto")
        data = rs.crypto.get_crypto_historicals(ticker,interval='day',span='year')
else:
        print("It's a stock")
        data = rs.stocks.get_stock_historicals(ticker, interval='day',span='year')

df = pd.DataFrame(data)


#Calculate Metrics
dates = pd.to_datetime(df['begins_at'])
high = df['high_price'].astype('float')
low = df['low_price'].astype('float')
close = df['close_price'].astype('float')
volume = df['volume']

sar = talib.SAR(high, low)
ema = talib.EMA(close,timeperiod=50)


#Visualize Output
plt.plot(dates,close)
plt.plot(dates,sar, marker='.')
plt.plot(dates,ema)


if ticker in ['BTC','ETH','DOGE','BSV','LTC','BCH','ETC']:
        if (sar[364] < close[364])  and (sar[363] < close[362]) and (sar[363] < close[362]):
            print("Buy " + ticker)
            #server.sendmail( 'Trade Signal', XXXXXXXXX, 'Buy ' + ticker)
        else:
            print("Sell " + ticker)
            #server.sendmail( 'Trade Signal', XXXXXXXXX, 'Sell ' + ticker)
else:
        if (sar[251] < close[251])  and (sar[250] < close[250]) and (sar[249] < close[249]):
            print("Buy " + ticker)
            #server.sendmail( 'Trade Signal',XXXXXXXXX, 'Buy ' + ticker)
        else:
            print("Sell " + ticker)
            #server.sendmail( 'Trade Signal', XXXXXXXXX, 'Sell ' + ticker)

print(sar)
print(close)