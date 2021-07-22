import matplotlib.pyplot as plt
import os
import pandas as pd
import json
from datetime import date, timedelta




def cagr_calc(start,end,ticker):
    """
    start - type:date - start date for CAGR Calc
    end - type:date - end date for CAGR Calc
    ticker - type:str - asset to calculate CAGR on.
    """
    #load price chart
    df = pd.read_csv(f'price/{ticker}_historic.csv')
    
    #convert to date object
    df['Date'] = pd.to_datetime(df['Date'],format='%Y-%m-%d')
    
    #parse start date and end date strings to datetime.
    l = pd.to_datetime(start, format='%Y-%m-%d')
    f = pd.to_datetime(end, format='%Y-%m-%d')

    
    #format start and end dates as YYYY-MM-DD
    startdate = f"{l}".replace("00:00:00","").replace(" ","")
    enddate = f"{f}".replace("00:00:00","").replace(" ","")
    
    #calculate how many years are between the start and end date
    N = ((f - l).days/365)
    
    #visual representation shown on front end
    timegap = f"{round(N,4)}"

    #Grabs the price for the start and end date
    L = float(df.loc[df['Date'] == l]['Price'].values[0])
    F = float(df.loc[df['Date'] == f]['Price'].values[0])

    #CAGR formula, represented as xxx.xx%
    CAGR = "{:.2%}".format(((F/L)**(1/N))-1)
    

    #plots historic price graph
    plt.plot(df.Date,df.Price)

    #assigns title of graph
    plt.title(f'{ticker} Historic Price')
    #Creates shaded red region between start and end
    plt.axvspan(l, f, alpha=0.2, color='red')

    #labels axis
    plt.xlabel(f'Time')
    plt.ylabel('Price (USD)')

    #assigns a master filepath on where to store images
    my_path = os.path.dirname(os.path.dirname(__file__))

    
    #saves image
    plt.savefig(f"{my_path}/app/static/images/{ticker}_{start}_{end}.png")
    #clears cache of plot tool
    plt.cla() 
    

    #final path where HTML should load from
    path = f'static/images/{ticker}_{start}_{end}.png'
    
    #foramts start and end price as $XXXX.XX
    finalprice = f"{'${:,.2f}'.format(F)}"
    startingprice = f"{'${:,.2f}'.format(L)}"
    readout = f"{CAGR}"

    #creates json payload to pass into HTML
    output = {}
    output['asset'] = ticker
    output['startdate'] = startdate
    output['enddate'] = enddate
    output['startingprice'] = startingprice
    output['finalprice'] = finalprice
    output['timegap'] = timegap
    output['readout'] = readout

    #master json that joins all assets in multiasset payload
    master = {}
    master[ticker]  = output

    output_path = path
    output_json = json.dumps(master)

    return output_json, output_path