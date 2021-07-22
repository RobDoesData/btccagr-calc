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
from datetime import date, timedelta
import json 

from cagr.calc import cagr_calc



#Enables saving of matplotlib charts as background process.
matplotlib.use('Agg')


app = Flask(__name__, template_folder="templates")


@app.route("/")
def homepage():

    #for timezone differences, it looks to two days ago to ensure uptime.
    end = date.today()- timedelta(days = 2)
    end =  end.strftime("%Y-%m-%d")
    

    #invokes default cagr calc for homepage between start of BTC price history, to latest date.
    payload, chartpath = cagr_calc('2010-07-18',end,'BTC')
    
    #manages payload to be passed to HTML page.
    payload = json.dumps(payload)
    payload = json.loads(payload)
    payload = json.loads(payload)
    
    
    #creates list of charts to be popluated on page.
    charts = []
    charts.append(chartpath) 
    return render_template('cagr.html',x=payload,charts=charts)


@app.route("/demo", methods = ['GET', 'POST'])
def demo_homepage():

    #grabs date fields from field submit
    start = request.form['start']
    end = request.form['end']


    #if the chart is only using BTC, load BTC only page.
    if request.form['ticker']  == "BTC":
        payload, chartpath = cagr_calc(start,end,'BTC')
        payload = json.dumps(payload).loads(payload).loads(payload)

        charts = []
        charts.append(chartpath) 
        return render_template('cagr.html',x=payload,charts=charts)
    else:
        group_chart = []
        group_payload = {}

        #loops across all 3 assets, and adds them to jsons/lists to be passed to html
        for i in ['BTC','GLD','SPY']:
            payload, chartpath = cagr_calc(start,end,i)
            payload = json.dumps(payload)
            payload = json.loads(payload)
            payload = json.loads(payload)
            group_chart.append(chartpath)
            group_payload.update(payload)
        
        return render_template('cagr.html',x=group_payload,charts=group_chart)
            
@app.route("/future", methods = ['GET', 'POST'])
def future_cagr():
    #loads historic BTC price chart
    df = pd.read_csv(f'price/BTC_historic.csv')

    #grabs most recent closing price of BTC
    last_close = int(df['Price'].iloc[-1])
    try:
        #checks to see if this is the first time loading the page.
        int(request.form['price'])
    except:
        #if there is no populated value, use default values
        price= int(last_close)
        time = 10
        cagr = 100
    else:
        #otherwise, use what was submitted into the form
        price = int(request.form['price'])
        time = float(request.form['time'])
        cagr = float(request.form['cagr'])
    #calculate future value of asset given inputs
    fv = price * ((cagr / 100 + 1)** time)

    return render_template('future.html',last_close=last_close,fv=fv,price=price,time=time,cagr=cagr)