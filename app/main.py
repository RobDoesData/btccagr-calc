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
        #startdate, enddate,timegap,finalprice,startingprice,readout,path = cagr_calc(start,end,ticker)
        #return render_template('cagr.html',startdate=startdate, enddate=enddate, timegap=timegap, finalprice=finalprice, startingprice=startingprice, readout=readout, path=path)
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
            

    #     btc_startdate, btc_enddate,btc_timegap,btc_finalprice,btc_startingprice,btc_readout,btc_path = cagr_calc(start,end,'BTC')
    #     gld_startdate, gld_enddate,gld_timegap,gld_finalprice,gld_startingprice,gld_readout,gld_path = cagr_calc(start,end,'GLD')
    #     spy_startdate, spy_enddate,spy_timegap,spy_finalprice,spy_startingprice,spy_readout,spy_path = cagr_calc(start,end,'SPY')


    #     return render_template('multi_cagr.html',startdate=startdate, enddate=enddate, timegap=timegap, finalprice=finalprice, startingprice=startingprice, readout=readout, path=path)