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



matplotlib.use('Agg')


app = Flask(__name__, template_folder="templates")


@app.route("/")
def homepage():
    today = date.today()
    yesterday = today - timedelta(days = 2)
    yesterday =  yesterday.strftime("%Y-%m-%d")
    

    payload, chartpath = cagr_calc('2010-07-18',yesterday,'BTC')
    
    payload = json.dumps(payload)
    payload = json.loads(payload)
    payload = json.loads(payload)
    
    charts = []
    charts.append(chartpath) 
    return render_template('cagr.html',x=payload,charts=charts)


@app.route("/demo", methods = ['GET', 'POST'])
def demo_homepage():
    start = request.form['start']
    end = request.form['end']

    if request.form['ticker']  == "BTC":
        payload, chartpath = cagr_calc(start,end,'BTC')
        payload = json.dumps(payload)
        payload = json.loads(payload)
        payload = json.loads(payload)
        charts = []
        charts.append(chartpath) 
        return render_template('cagr.html',x=payload,charts=charts)
    else:
        group_chart = []
        group_payload = {}
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
    df = pd.read_csv(f'price/BTC_historic.csv')
    last_close = df['Price'].iloc[-1]
    last_close = int(float(last_close))
    try:
        request.form['price']
    except:
        price= int(last_close)
        time = 10
        cagr = 100
    else:
        price = request.form['price']
        time = float(request.form['time'])
        cagr = float(request.form['cagr'])

        price = int(float(price))
    fv = price * ((cagr / 100 + 1)** time)

    if price!=last_close:
        price = last_close

    return render_template('future.html',last_close=last_close,fv=fv,price=price,time=time,cagr=cagr)