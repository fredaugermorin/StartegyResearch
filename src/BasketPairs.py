# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 13:54:08 2016

@author: fredaugermorin - Credits to Michael Halls Moore @ Quanstart
"""    
if __name__ == "__main__":
    import quandl as qdl
    import statsmodels.tsa.stattools as stm
    import matplotlib.pyplot as plt
    import matplotlib
    import pandas as pd
    import numpy as np
    matplotlib.style.use('ggplot')
    
    qdl.ApiConfig.api_key = 'ykCFLxj3ofyyn_4s3EGu'    
    
    mesTickers = ['YAHOO/TO_NA','YAHOO/TO_BMO']
    
    mesDates = ['2007-01-03','2016-08-06']
    
    myData = qdl.get(mesTickers,start_date=mesDates[0],end_date =mesDates[1])      
  
    i = 1
    chartHeight = len(mesTickers)     
    
    for ticker in mesTickers:
        plt.subplot(chartHeight,2,i)
        plt.plot(myData[ticker+' - Adjusted Close'])
        i = i + 1
        plt.subplot(chartHeight,2,i)
        myData[ticker +' - Log Return'] = np.log(myData[ticker+' - Adjusted Close']) - np.log(myData[ticker +' - Adjusted Close'].shift(1))
        plt.plot(myData[ticker+' - Log Return'])
        i = i + 1
    
    plt.show()
    
    print("++++++++ " + mesTickers[0] + " In Level++++++++\n")
    print(stm.adfuller(myData[mesTickers[0]+' - Adjusted Close'],regression='ct'))
    print("++++++++ " + mesTickers[0] + " In Diff ++++++++\n")
    print(stm.adfuller(myData[mesTickers[0]+' - Log Return'][1:], regression='c'))
    
    print("++++++++ " + mesTickers[1] + " In Level++++++++\n")
    print(stm.adfuller(myData[mesTickers[1]+' - Adjusted Close'],regression='ct'))
    print("++++++++ " + mesTickers[1] + " In Diff ++++++++\n")
    print(stm.adfuller(myData[mesTickers[1]+' - Log Return'][1:], regression='c'))
    
    
    plt.scatter(myData['YAHOO/TO_NA - Adjusted Close'],myData['YAHOO/TO_BMO - Adjusted Close'])
    plt.show()
    
    # Both series are I(1) lets find the hedge ratio
    # we need engle and granger to make sure they are cointegrated
    # following quanstart, we will simply regress prices and find hedge ratio
    
    model1 = pd.ols(y=myData['YAHOO/TO_NA - Adjusted Close'],x=myData['YAHOO/TO_BMO - Adjusted Close'])
    model2 = pd.ols(y=myData['YAHOO/TO_BMO - Adjusted Close'],x=myData['YAHOO/TO_NA - Adjusted Close'])
    res1=model1.resid
    res2=model2.resid
    print(model1)
    print(model2)    
    
    
    print(stm.adfuller(res1, regression='c'))
    print(stm.adfuller(res2, regression='c'))
    # Based on ADF test statistic we take the first regression as the test statistic is smaller(more neagative)
    #Plot residuals and 95% confidence levels    
    ax = res1.plot()    
    top = res1 + 1.96*model1.rmse
    top.plot(ax=ax)
    bot = res1 - 1.96*model1.rmse
    bot.plot(ax=ax)
    plt.title('Residuals with confidence interval')
    plt.show()
    
    # If our prevision implied by the model is greater than the 95% bounds
    # we long/short the spread using our headge ration implied by the regression
    print(model1.beta)    
    hr = model1.beta[0]
    a = model1.beta[1]    
    myData['Top bound'] = top
    myData['Bot bound'] = bot
    myData['Prevision t+1'] = (a + hr*myData['YAHOO/TO_BMO - Adjusted Close'].shift(1)) - myData['YAHOO/TO_NA - Adjusted Close']
    
    
    plt.plot(myData[['Prevision t+1','Top bound','Bot bound']])
    plt.legend(['Forecast','95% Top Bound','95% Bottom Bound'])
    plt.title('Pairs Trade NA/BMO - Signal Generation')
    plt.show()
    
    # generate additional columns to help in backtest    
    
    myData['Signal'] = 0 #simple preallocation

    myData.loc[myData['Prevision t+1'] > myData['Top bound'].shift(1),['Signal']] = 1
    myData.loc[myData['Prevision t+1'] < myData['Bot bound'].shift(1),['Signal']] = -1

    
    myData['Hold'] = 1
    
    myData.loc[myData['Signal'] != myData['Signal'].shift(1),['Hold']] = 0
   
    initCapital = 100000
    myData['Units'] = initCapital // np.abs(-1*myData['YAHOO/TO_NA - Adjusted Close']  + hr*myData['YAHOO/TO_BMO - Adjusted Close'])
    myData['Position'] = myData['Units'] * ((-1*myData['YAHOO/TO_NA - Adjusted Close']  + hr*myData['YAHOO/TO_BMO - Adjusted Close']) * myData['Signal'])
    myData['PnL'] = myData['Hold'] * (myData['Position'].diff(1))
    myData['Cash'] = initCapital + np.cumsum(myData['PnL'])

    plt.subplot(211)
    plt.plot(myData['Cash'])
    plt.title('Evolution of ' +str(initCapital) +' $ allocated to trade')  
    plt.subplot(212)
    plt.plot(myData['PnL'])
    plt.title('Evolution of PnL per trade')    
    plt.show()
        
            
        
            

    