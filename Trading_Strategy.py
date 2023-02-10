from blueshift.api import(    symbol,
                            order_target_percent,
                            schedule_function,
                            date_rules,
                            time_rules,
                            data
                       )
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

import talib ## to get the RSI 

def initialize(context):
    """
        A function to define things to do at the start of the strategy
    """
    
    # universe selection
    context.long_portfolio = [
                               symbol('DIVISLAB'),
                               symbol('SUNPHARMA'),
                               symbol('MARUTI'),
                               symbol('AMARAJABAT'),
                               symbol('BPCL'),                               
                               symbol('BAJFINANCE'),
                               symbol('HDFCBANK'),
                               symbol('ASIANPAINT'),
                               symbol('TCS')
                             ]
    
    # Call rebalance function every trading day
    schedule_function(strategy,
                      date_rules.every_day(),
                      time_rules.market_close(hours=0, minutes=30))


def strategy(context, data):
    """
        A function to rebalance the portfolio, passed on to the call
        of schedule_function above.
    """
    for security in context.long_portfolio:
        lows = data.history(security, 'low', 20, '1d').dropna()
        highs = data.history(security, 'high', 20, '1d').dropna()
        current_price = data.current(security, 'price').dropna()
        
        low_reg = LinearRegression().fit(np.array(range(20)).reshape(-1,1), lows)
        high_reg = LinearRegression().fit(np.array(range(20)).reshape(-1,1), highs)
        
        low_fit = low_reg.predict(np.array([20]).reshape(-1,1))
        high_fit = high_reg.predict(np.array([20]).reshape(-1,1))
        
        moving_average_10 = data.history(security, 'price', 10, '1d').mean()
        moving_average_20 = data.history(security, 'price', 20, '1d').mean()

        rsi = talib.rsi(price,timeperiod = 14)
                
        strong_upwards = False
        strong_downwwards = False

        if moving_average_10 > moving_average_20 or rsi<35:
          strong_upwards = True
        if moving_average_20 <moving_average_20 or rsi>65:
          strong_downwards = True
        
 
        if ((current_price < fit_low) and not strong_downwards):
            order_target_percent(security, 1.0/10)
        elif ((current_price < fit_low) and strong_downwards):
            order_target_percent(security,0)
        

        elif (current_price > fit_high) and not strong_upwards:
            order_target_percent(security, 0)
        else:
            order_target_percent(security,1.0/10)