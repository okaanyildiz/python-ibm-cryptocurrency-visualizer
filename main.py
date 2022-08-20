# !pip install pycoingecko
# !pip install plotly
# !pip install mplfinance

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.offline import plot
import matplotlib.pyplot as plt
import datetime
from pycoingecko import CoinGeckoAPI
from mplfinance.original_flavor import candlestick2_ohlc


# Get the 30 days data from CoinGeckoAPI
cg = CoinGeckoAPI()

# id: coin name, vs_currency: currency, days: duration of the data
bitcoin_data = cg.get_coin_market_chart_by_id(
    id='bitcoin', vs_currency='usd', days=30)

# Select sample price data
bitcoin_price_data = bitcoin_data['prices']
bitcoin_price_data[0:5]

# Create the Pandas data frame from the sample data
data = pd.DataFrame(bitcoin_price_data, columns=['TimeStamp', 'Price'])

# Convert the timestamp to datetime
# Save it as a column called Date.
# We will map our unix_to_datetime to each timestamp and convert it to a readable datetime.
data['date'] = data['TimeStamp'].apply(
    lambda d: datetime.date.fromtimestamp(d/1000.0))

# Group the dataset by the Date
# Find the min, max, open, and close for the candlesticks
candlestick_data = data.groupby(data.date, as_index=False).agg(
    {"Price": ['min', 'max', 'first', 'last']})

# Use plotly to create the Candlestick Chart
fig = go.Figure(data=[go.Candlestick(x=candlestick_data['date'],
                open=candlestick_data['Price']['first'],
                high=candlestick_data['Price']['max'],
                low=candlestick_data['Price']['min'],
                close=candlestick_data['Price']['last'])
                      ])

fig.update_layout(xaxis_rangeslider_visible=False)

fig.show()
