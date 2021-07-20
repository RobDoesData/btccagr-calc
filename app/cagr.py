import matplotlib.pyplot as plt
import os
import pandas as pd


def cagr_calc():
    df = pd.read_csv('btcprice.csv')
    df['Date'] = pd.to_datetime(df['Date'],format='%m/%d/%y')
    df.columns = ['Date','Price']
    
    l = pd.to_datetime("2010-07-15", format='%Y-%m-%d')
    f = pd.to_datetime("2021-07-18", format='%Y-%m-%d')
    
    startdate = f"Starting date {l}".replace("00:00:00","")
    enddate = f"End date {f}".replace("00:00:00","")
    N = ((f - l).days/365)
    timegap = f"Years between start and end {round(N,2)}"
    L = float(df.loc[df['Date'] == l]['Price'].values[0])
    F = float(df.loc[df['Date'] == f]['Price'].values[0])
    CAGR = "{:.0%}".format(((F/L)**(1/N)))
    
    plt.plot(df.Time,df.Price)
    plt.title('Bitcoin Historic Price')
    plt.axvspan(l, f, alpha=0.5, color='red')
    plt.xlabel('BTC/USD Price')
    plt.ylabel('Price (USD)')
    #plt.yscale("log")
    # plt.show()
    my_path = os.path.dirname(os.path.realpath(__file__))
    plt.savefig(f"{my_path}/static/images/default.png")
    plt.cla() 
    
    path = f'static/images/default.png'
    finalprice = f"Final Price is: {'${:,.2f}'.format(F)}"
    startingprice = f"Starting Price is: {'${:,.2f}'.format(L)}"
    readout = f"The CAGR between {f.date()} and {l.date()} is {CAGR}"
    return startdate, enddate, timegap, finalprice, startingprice, readout, path