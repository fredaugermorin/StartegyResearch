# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 13:54:08 2016

@author: FRED
"""    
if __name__ == "__main__":
    import quandl as qdl
    import statsmodels.tsa.stattools as stm
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    
    qdl.ApiConfig.api_key = 'ykCFLxj3ofyyn_4s3EGu'    
    
    mesTickers = ['YAHOO/TO_NA','YAHOO/TO_BMO']
    
    mesDates = ['2007-01-02','2016-08-06']
    
    myData = qdl.get(mesTickers,start_date=mesDates[0],end_date =mesDates[1])    
    print(myData)
   
    
    i = 1        
    for ticker in mesTickers:
        plt.subplot(2,2,i)
        plt.plot(myData[ticker+' - Adjusted Close'])
        i = i + 1
        plt.subplot(3,2,i)
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
    
    plt.figure()
    plt.scatter(myData['YAHOO/TO_NA - Adjusted Close'],myData['YAHOO/TO_BMO - Adjusted Close'])
    # Both series are I(1) lets find the hedge ratio
    
    
    