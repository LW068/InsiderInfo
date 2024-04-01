import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime
import time

# Function to fetch real-time data from Yahoo Finance
def get_real_time_data(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period='1d', interval='1m')
    return data

# Function to update Plotly candlestick chart
def update_chart(fig, data):
    fig.update_traces(x=data.index,
                      open=data['Open'],
                      high=data['High'],
                      low=data['Low'],
                      close=data['Close'])

# Define the stock symbol
symbol = 'AAPL'

# Create initial Plotly candlestick chart
initial_data = get_real_time_data(symbol)
fig = go.Figure(data=[go.Candlestick(x=initial_data.index,
                                     open=initial_data['Open'],
                                     high=initial_data['High'],
                                     low=initial_data['Low'],
                                     close=initial_data['Close'])])

fig.update_layout(title=f'Real-Time Candlestick Chart for {symbol}')

# Update the chart every minute
while True:
    real_time_data = get_real_time_data(symbol)
    update_chart(fig, real_time_data)
    fig.write_html('realtime_candlestick.html') # Write the updated chart to an HTML file
    time.sleep(30)  # Wait for 60 seconds before updating the chart again
