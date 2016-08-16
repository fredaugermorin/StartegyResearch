# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 16:10:24 2016

@author: faugermorin
@brief: backtest ewma trading strategy in unflexible manner
"""
import quandl as qdl

import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np

matplotlib.style.use('ggplot')
    
qdl.ApiConfig.api_key = 'ykCFLxj3ofyyn_4s3EGu'    

if __name__ == '__main__':
    shortEWMA = 10
    longEWMA = 50
    ticker = ['YAHOO/TO_SU']
    myDates = ['2007-01-03','2016-08-06']
    
    myData = qdl.get(ticker,start_date=myDates[0],end_date = myDates[1]) 
    
   #myData[ticker[0] + ' - Returns'] = np.log(myData[ticker[0] + ' - Adjusted Close'] / myData[ticker[0] + ' - Adjusted Close'].shift(1))
    myData['Short EWMA'] = pd.ewma(myData[ticker[0]+' - Adjusted Close'],span=shortEWMA,min_periods = shortEWMA)  
    myData['Long EWMA'] = pd.ewma(myData[ticker[0]+' - Adjusted Close'],span=longEWMA,min_periods =longEWMA)  
    
    toplot = [ticker[0]+' - Adjusted Close','Short EWMA','Long EWMA']
    for line in toplot:
        plt.plot(myData[line])
    plt.legend(toplot)
    plt.show()
   