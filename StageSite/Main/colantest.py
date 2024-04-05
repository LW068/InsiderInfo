import dash
from dash import dcc, html, Input, Output
import yfinance as yf
import plotly.graph_objects as go

# Function to fetch real-time data from Yahoo Finance
def get_real_time_data(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period='2h', interval='1m')
    return data

# Function to create a styled Plotly candlestick chart
def update_chart(symbol):
    data = get_real_time_data(symbol)
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                                         open=data['Open'],
                                         high=data['High'],
                                         low=data['Low'],
                                         close=data['Close'],
                                         increasing_line_color='#3344DC',
                                         decreasing_line_color='#DC2B46')])

    # Update the figure with the desired layout properties
    fig.update_layout(
        title=f'Candlestick Chart for {symbol}',
        xaxis_title='Date',
        yaxis_title='Price',
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background for the plot
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background for the paper
        xaxis=dict(
            gridcolor='white',  # Grid color set to white for contrast
            rangeslider=dict(visible=False)  # Hiding the rangeslider
        ),
        yaxis=dict(gridcolor='white'),  # White grid lines for y-axis
        font=dict(family='Inter', size=12, color='white')  # Custom font settings
    )
    return fig

# Create Dash app
app = dash.Dash(__name__)

# Define the stock symbol
symbol = 'AAPL'

# Define the layout of the app
app.layout = html.Div([
    dcc.Graph(
        id='live-update-graph',
        config={'displayModeBar': False},  # Hides the modebar
        style={'width': '100%', 'height': '100%'}
    ),
    dcc.Interval(
        id='interval-component',
        interval=30*1000,  # in milliseconds
        n_intervals=0
    )
])

# Define the callback to update the graph
@app.callback(
    Output('live-update-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph_live(n_intervals):
    return update_chart(symbol)

if __name__ == '__main__':
    app.run_server(host='74.208.70.17', port=8050, debug=False)  # Set debug to False for production
    app.run_server(host='https://insiderinfor.app', port=8050, debug=False)
