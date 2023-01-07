import bt
import yfinance as yf
import talib as ta
import matplotlib.pyplot as plt

price_data = yf.Ticker('spy').history(period='12mo', interval='1d')
price_data = price_data[['Open', 'Low', 'High', 'Close', 'Volume']]

# sma = ta.SMA(price_data.Close, 20)
sma = price_data.rolling(20).mean()

strat = bt.Strategy('Simple SMA', [
    bt.algos.SelectWhere(price_data > sma),
    bt.algos.WeighEqually(),
    bt.algos.Rebalance()
])

# Create the backtest and run it
bt_backtest = bt.Backtest(strat, price_data)
bt_result = bt.run(bt_backtest)
# Plot the backtest result
bt_result.plot(title='Backtest result')
plt.show()
