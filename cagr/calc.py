import matplotlib.pyplot as plt
import os
import pandas as pd
import json
from datetime import date, timedelta


def cagr_calc(start,end,ticker):
    df = pd.read_csv(f'price/{ticker}_historic.csv')
    df['Date'] = pd.to_datetime(df['Date'],format='%Y-%m-%d')
    
    if ticker=='BTC':
        l = pd.to_datetime(start, format='%Y-%m-%d')
        f = pd.to_datetime(end, format='%Y-%m-%d')
    else:
        
        l = pd.to_datetime(start, format='%Y-%m-%d')
        while not bool(len(pd.bdate_range(l, l))):
            l = l + timedelta(days = 1)
        
        f = pd.to_datetime(end, format='%Y-%m-%d')
        while not bool(len(pd.bdate_range(f, f))):
            f = f - timedelta(days = 1)

    
    startdate = f"{l}".replace("00:00:00","").replace(" ","")
    enddate = f"{f}".replace("00:00:00","").replace(" ","")
    N = ((f - l).days/365)
    timegap = f"{round(N,2)}"
    L = float(df.loc[df['Date'] == l]['Price'].values[0])
    F = float(df.loc[df['Date'] == f]['Price'].values[0])
    CAGR = "{:.0%}".format(((F/L)**(1/N)))
    
    plt.plot(df.Date,df.Price)
    plt.title(f'{ticker} Historic Price')
    


    plt.axvspan(l, f, alpha=0.2, color='red')
    plt.xlabel(f'Time')
    plt.ylabel('Price (USD)')
    my_path = os.path.dirname(os.path.dirname(__file__))

    plt.savefig(f"{my_path}/app/static/images/{ticker}_{start}_{end}.png")
    plt.cla() 
    
    path = f'static/images/{ticker}_{start}_{end}.png'
    finalprice = f"{'${:,.2f}'.format(F)}"
    startingprice = f"{'${:,.2f}'.format(L)}"
    readout = f"{CAGR}"

    output = {}
    output['asset'] = ticker
    output['startdate'] = startdate
    output['enddate'] = enddate
    output['startingprice'] = startingprice
    output['finalprice'] = finalprice
    output['timegap'] = timegap
    output['readout'] = readout

    master = {}
    master[ticker]  = output

    output_path = path

    output_json = json.dumps(master)

    return output_json, output_path