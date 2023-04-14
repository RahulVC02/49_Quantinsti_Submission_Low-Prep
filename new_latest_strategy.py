from blueshift.api import(    symbol,
                            order_target_percent,
                            schedule_function,
                            date_rules,
                            time_rules
                       )
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

import talib ## to get the RSI 
day =0


def initialize(context):
    """
        A function to define things to do at the start of the strategy
    """
    
    # universe selection
    print("in initialize")
    
    context.long_portfolio = [
                               symbol("MARUTI"),
                               symbol("ULTRACEMCO"),
                               symbol("EICHERMOT"),
                               symbol("HEROMOTOCO"),
                               symbol("DRREDDY"), 
                               symbol("BAJFINANCE"),
                               symbol("INDUSINDBK"),
                               symbol("HDFC"),
                               symbol("GRASIM")
                             ]
    
    # Call rebalance function every trading day
    
    schedule_function(strategy,
                      date_rules.every_day(),
                      time_rules.market_open(hours=0, minutes=30))


def strategy(context, data):
    """
        A function to rebalance the portfolio, passed on to the call
        of schedule_function above.
    """
    global day
    day = day + 1


    
    
    for security in context.long_portfolio:

        if(day<21):
            order_target_percent(security,0)
            return


        lows = data.history(security, "low", 20, "1d").dropna()
        highs = data.history(security, "high", 20, "1d").dropna()
        print("highs:", highs)
        print("type(highs):", type(highs))
        current_price = data.current(security, "open")
        
        low_reg = LinearRegression().fit(np.array(range(20)).reshape(-1,1), lows)
        high_reg = LinearRegression().fit(np.array(range(20)).reshape(-1,1), highs)
        
        low_fit = low_reg.predict(np.array([20]).reshape(-1,1))
        high_fit = high_reg.predict(np.array([20]).reshape(-1,1))
        
        
        moving_average_10 = data.history(security, "open", 10, "1d")
        if not moving_average_10.empty:
            moving_average_10 = moving_average_10.mean()
        else:
            moving_average_10 = 0

        moving_average_20 = data.history(security, "open", 20, "1d")
        if not moving_average_20.empty:
            moving_average_20 = moving_average_20.mean()
        else:
            moving_average_20 = 0
        

        past_prices = data.history(security, "open", 14, "1d").dropna()
        rsi = talib.RSI(past_prices, timeperiod = 14)
                
        strong_upwards = False
        strong_downwards = False
# moving_average_10 > moving_average_20 and
        if  moving_average_10 < moving_average_20 and rsi[0]<35:
          strong_upwards = True
# moving_average_10 < moving_average_20 and 
        if moving_average_10 < moving_average_20 and rsi[0]>65:
          strong_downwards = True


        if current_price<=low_fit[0]:
            
            if(strong_downwards):
                order_target_percent(security,0)
                continue
            else:
                order_target_percent(security, 1.0/10)
                continue


        if current_price>=high_fit[0] :
            
            if(strong_upwards):
                order_target_percent(security, 1.5/10)
                continue
            else:
                order_target_percent(security, 0)
                continue
