from backtesting import Backtest
import yfinance as yf
import matplotlib.pyplot as plt
import backtesting
from backtesting import Strategy
from backtesting.lib import crossover

import pandas as pd
import talib as ta

price_data = yf.Ticker('spy').history(period='12mo', interval='1d')

backtesting.set_bokeh_output(notebook=False)


class SmaCross(Strategy):
    # Define the two MA lags as *class variables*
    # for later optimization
    n1 = 10
    n2 = 20

    def init(self):
        super().init()
        # Precompute the two moving averages
        self.sma1 = self.I(ta.SMA, self.data.Close, self.n1)
        self.sma2 = self.I(ta.SMA, self.data.Close, self.n2)

    def next(self):
        super().next()
        # If sma1 crosses above sma2, close any existing
        # short trades, and buy the asset
        if crossover(self.sma1, self.sma2):
            self.position.close()
            self.buy()

        # Else, if sma1 crosses below sma2, close any existing
        # long trades, and sell the asset
        elif crossover(self.sma2, self.sma1):
            self.position.close()
            self.sell()


bt = Backtest(price_data, SmaCross, cash=1_000, commission=.002)

stats = bt.run()

bt.plot()
