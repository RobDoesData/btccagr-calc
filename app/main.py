from flask import Flask, render_template,request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
import datetime
import uuid
import random
import os
import io
import base64
import matplotlib


matplotlib.use('Agg')


app = Flask(__name__)


@app.route("/")
def homepage():
    df = pd.read_csv('btcprice.csv')
    df['Time'] = pd.to_datetime(df['Time'],format='%m/%d/%y')
    df.columns = ['Time','Price']
    
    l = pd.to_datetime("2010-07-15", format='%Y-%m-%d')
    f = pd.to_datetime("2021-07-18", format='%Y-%m-%d')
    
    startdate = f"Starting date {l}".replace("00:00:00","")
    enddate = f"End date {f}".replace("00:00:00","")
    N = ((f - l).days/365)
    timegap = f"Years between start and end {round(N,2)}"
    L = float(df.loc[df['Time'] == l]['Price'].values[0])
    F = float(df.loc[df['Time'] == f]['Price'].values[0])
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

    return render_template('cagr.html',startdate=startdate, enddate=enddate, timegap=timegap, finalprice=finalprice, startingprice=startingprice, readout=readout, chart=path)


@app.route("/demo", methods = ['GET', 'POST'])
def demo_homepage():
    df = pd.read_csv('btcprice.csv')
    df['Time'] = pd.to_datetime(df['Time'],format='%m/%d/%y')
    df.columns = ['Time','Price']
    start = request.form['start']
    end = request.form['end']

    l = pd.to_datetime(start, format='%Y-%m-%d')
    f = pd.to_datetime(end, format='%Y-%m-%d')
    
    startdate = f"Starting date {l}".replace("00:00:00","")
    enddate = f"End date {f}".replace("00:00:00","")
    N = ((f - l).days/365)
    timegap = f"Years between start and end {round(N,2)}"
    L = float(df.loc[df['Time'] == l]['Price'].values[0])
    F = float(df.loc[df['Time'] == f]['Price'].values[0])
    CAGR = "{:.0%}".format(((F/L)**(1/N)))
    
    plt.plot(df.Time,df.Price)
    plt.title('Bitcoin Historic Price')
    plt.axvspan(l, f, alpha=0.5, color='red')
    plt.xlabel('BTC/USD Price')
    plt.ylabel('Price (USD)')
    img_uuid = uuid.uuid4()
    my_path = os.path.dirname(os.path.realpath(__file__))
    
    plt.savefig(f"{my_path}/static/images/{img_uuid}.png")
    plt.cla() 

    path = f"static/images/{img_uuid}.png"
    finalprice = f"Final Price is: {'${:,.2f}'.format(F)}"
    startingprice = f"Starting Price is: {'${:,.2f}'.format(L)}"
    readout = f"The CAGR between {l.date()} and {f.date()} is {CAGR}"

    return render_template('cagr.html',startdate=startdate, enddate=enddate, timegap=timegap, finalprice=finalprice, startingprice=startingprice, readout=readout, chart=path)
