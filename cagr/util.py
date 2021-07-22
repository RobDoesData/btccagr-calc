import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import os
import json
import yfinance as yf

from datetime import date, timedelta
import json
import requests
import warnings


def coindesk_scrape(start,end):
    """
    start - date - start date 
    end - date - end date

    date format is yyyy-mm-dd
    Uses coindesk API to grab daily BTC price.
    """
    
    #API Endpoint
    url = f'https://api.coindesk.com/v1/bpi/historical/close.json?start={start}&end={end}'
    r = requests.get(url) 
    data = r.json()
    
    #parses API output for only the date and daily price price
    data = pd.DataFrame.from_dict(data).reset_index()[['index','bpi']]
    data.columns = ['Date','Price']
    
    #drops metadata fields that show as N/A
    data = data.dropna()
    #saves to .csv
    data.to_csv('BTC_historic.csv',index=False)
    return 

def yfinance_scrape(ticker_name):
    """
    Uses the yahoo finance API to get the daily  asset prices for a stock.

    ticker_name - str - stock ticker to aggregate data of
    """


    today = date.today()
    
    #this is the earlist date we have BTC price, so it is where other charts begin
    sdate = date(2010, 7, 14)   
    edate = date(today.year, today.month, today.day)

    #lists all dates from starting BTC price date to today
    #this mater list of all dates is created to align with BTC price chart
    #unfortunately fiat markets aren't open 24/7
    date_list = pd.date_range(sdate,edate,freq='d')

    #creates a pandas dataframe from the list of dates
    date_series = pd.Series(date_list).reset_index().drop('index',axis=1).rename(columns={0:"Date"})

    
    #Grabs daily close price of input stock ticker for avaiable date range
    ticker = yf.Ticker(ticker_name)
    ticker_history = ticker.history(start="2010-07-14",  end=today)
    ticker_history = ticker_history.reset_index()[['Date','Close']]
    ticker_history.columns = ['Date','Price']

    #merges the market activity with the master date list
    #for dates where there is no market close, it will use the previous day's value.
    date_series = date_series.merge(ticker_history,how='left').fillna(method='ffill')
    
    #saves to csv
    date_series.to_csv(f"{ticker_name}_historic.csv",index=False)
    return    