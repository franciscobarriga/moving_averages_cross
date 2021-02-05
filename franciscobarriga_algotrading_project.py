# -*- coding: utf-8 -*-
"""
FranciscoBarriga_AlgoTrading_Project

### Algo Trading Simulator!

## A very basic *algo trading* simulator, where you can input a stock ticker, and it will automtically calculate the crosses between the 50 and 20 day moving averages as a momentum advantage of when to buy or sell a stock, it is a widely popular technical indicator used by traders

"""
# Importing important libraries in order to fully take advantage of Python to trade
!pip install watermark
!pip install yahoo_finance
!pip install pandas_datareader
!pip install quandl

import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import watermark
import yahoo_finance
import quandl

#Loading the stock info
ticker = input("Insert the ticker here to explore the stock:").upper()

#Dates are limited to available information within Yahoo! Finance
beginning_year = int(input("Write your beginning year here:"))
beginning_month = int(input("Write your beginning month here:"))
beginning_day = int(input("Write your beginning day here:"))

ending_year = int(input("Write your ending year here:"))
ending_month = int(input("Write your ending month here:"))
ending_day = int(input("Write your ending day here:"))

print(f"{ticker} stock information from {beginning_year,beginning_month,beginning_day} up to {ending_year,ending_month,ending_day}")

stock = pdr.get_data_yahoo(ticker, 
                          start=datetime.datetime(beginning_year,beginning_month, beginning_day), 
                          end=datetime.datetime(ending_year,ending_month, ending_day))
stock.head()

#Inspecting the dataset
stock.info()

#Visualizing
plt.style.use("dark_background")
plt.figure(figsize=(12.5,5))
plt.plot(stock["Adj Close"], label = ticker, color = "blue")
plt.title(f"{ticker.upper()} Adj. Close Price History")
plt.xlabel(f"{beginning_year,beginning_month,beginning_day} up to {ending_year,ending_month,ending_day}")
plt.ylabel("Asj. Close Price USD ($)")
plt.legend(loc = "upper left")
plt.grid(True)
plt.show()

#Create the SMAs (Simple Moving Averages)
SMA13 = pd.DataFrame()
SMA13["Adj Close Price"] = stock["Adj Close"].rolling(window= 13).mean()
SMA20 = pd.DataFrame()
SMA20["Adj Close Price"] = stock["Adj Close"].rolling(window= 20).mean()
SMA50 = pd.DataFrame()
SMA50["Adj Close Price"] = stock["Adj Close"].rolling(window= 50).mean()
SMA200 = pd.DataFrame()
SMA200["Adj Close Price"] = stock["Adj Close"].rolling(window= 200).mean()

#Visualizing
plt.style.use("dark_background")
plt.figure(figsize=(12.5,5))
plt.plot(stock["Adj Close"], label = ticker, color = "blue")
plt.plot(SMA13["Adj Close Price"], label = "SMA13", color = "limegreen")
plt.plot(SMA20["Adj Close Price"], label = "SMA20", color = "magenta")
plt.plot(SMA50["Adj Close Price"], label = "SMA50", color = "moccasin")
plt.plot(SMA200["Adj Close Price"], label = "SMA200", color = "red")

plt.title(f"{ticker.upper()} Adj. Close Price History")
plt.xlabel(f"{beginning_year,beginning_month,beginning_day} up to {ending_year,ending_month,ending_day}")
plt.ylabel("Asj. Close Price USD ($)")
plt.legend(loc = "upper left")
plt.grid(True)
plt.show()

"""

###In theory, a good signal to buy would be when the stock is above its 200 day MA and the 50 day MA, and the crossover between the 13 and 30 day MA is just about to happen 

## This is merely a momentum trading strategy, and by no means is a sound investment idea, but mereyly a speculation of the price regarding various variables

"""

#Creating a Data Frame with all the Moving Averages in order to segment and analyze when they cross
data = pd.DataFrame()
data[ticker] = stock["Adj Close"]
data["SMA13"] = SMA13["Adj Close Price"]
data["SMA20"] = SMA20["Adj Close Price"]
data["SMA50"] = SMA50["Adj Close Price"]
data["SMA200"] = SMA200["Adj Close Price"]
data.head()

#Create a function to signal when to buy and sell the security
def buy_sell(data):
  price_to_buy = []
  price_to_sell = []
  flag = -1

  for i in range(len(data)):
    if data["SMA20"][i] > data["SMA50"][i]:
      if flag!= 1:
        price_to_buy.append(data[ticker][i])
        price_to_sell.append(np.nan)
        flag = 1
      else:
        price_to_buy.append(np.nan)
        price_to_sell.append(np.nan)
    elif data["SMA20"][i] < data["SMA50"][i]:
      if flag != 0:
          price_to_buy.append(np.nan)
          price_to_sell.append(data[ticker][i])
          flag = 0
      else:
          price_to_buy.append(np.nan)
          price_to_sell.append(np.nan)
    else:
      price_to_buy.append(np.nan)
      price_to_sell.append(np.nan)


  return(price_to_buy,price_to_sell)

#Store buy and sell data into a variable
buy_sell = buy_sell(data)
data["Buy_Signal_Price"] = buy_sell[0]
data["Sell_Signal_Price"] = buy_sell[1]

#Show the data
data

"""
# Because the data we have is from the daily adjusted price, we have to use the 20 and 50 day MA, they are regarded as the defacto movement detectors on the daily chart.

#### This is only with one stock, and we could add more studied in order to determine the perfect time when to buy and when to sell, like for example more mommentum indicators such as the MACD and the RSI, but it is a good starting point nonetheless.

#### If there is not enough days to create the SMA20 nor SMA50, the final graph will show an error (because the extracted data is daily)
"""

#Visualize
plt.figure(figsize=(12.5,5))
plt.plot(data.iloc[:,0], label = ticker, color = "cyan", alpha = 0.2)
plt.plot(data["SMA20"], label = "SMA20", color = "limegreen", alpha = 0.5)
plt.plot(data["SMA50"], label = "SMA50", color = "magenta", alpha = 0.5)
plt.scatter(data.index, data["Buy_Signal_Price"], label = "BUY!", marker = "^", color = "green")
plt.scatter(data.index, data["Sell_Signal_Price"], label = "SELL!", marker = "v", color ="red")
plt.title(f"{ticker} Adj. Close Price History of possible buy and sell signals regarding MA crossovers")
plt.ylabel("Asj. Close Price USD ($)")
plt.legend(loc = "upper left")
plt.grid(True)
plt.show()

