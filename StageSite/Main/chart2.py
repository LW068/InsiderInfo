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
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        increasing_line_color='#3344DC',
        decreasing_line_color='#DC2B46'
    )])

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

# Function to get current price
def get_current_price(symbol):
    stock = yf.Ticker(symbol)
    current_price = stock.history(period='1d')['Close'][-1]
    return current_price

# Create Dash app
app = dash.Dash(__name__)

# Define a list to store the submitted tickers
submitted_tickers = []

# Define the layout of the app
app.layout = html.Div(style={'backgroundColor': 'black', 'display': 'flex', 'alignItems': 'center'}, children=[
    html.Div(style={'textAlign': 'center', 'marginRight': '20px'}, children=[
        html.Div([
            dcc.Input(
                id='stock-input',
                type='text',
                value='AAPL',
                placeholder='Enter Ticker Symbol...',
                style={'width': '100px'}
            ),
            html.Button('Submit', id='submit-button', n_clicks=0)
        ]),
        html.Div(id='ticker-history', style={'color': 'white', 'fontSize': 16, 'fontFamily': 'Inter'}),
        html.Div(id='ticker-symbol', style={'color': 'white', 'fontSize': 24, 'fontFamily': 'Inter'}),
        html.Div(id='current-price', style={'color': 'white', 'fontSize': 24, 'fontFamily': 'Inter'}),
    ]),
    html.Div([
        dcc.Graph(
            id='live-update-graph',
            config={'displayModeBar': False},  # Hides the modebar
            style={'width': '100%', 'height': '80vh'}  # Set width to 100% and height to 80% of viewport height
        ),
        dcc.Interval(
            id='interval-component',
            interval=30*1000,  # in milliseconds
            n_intervals=0
        )
    ], style={'flex': '3'})
])

# Define the callback to update the graph and display current price
@app.callback(
    [Output('live-update-graph', 'figure'),
     Output('ticker-history', 'children'),
     Output('ticker-symbol', 'children'),
     Output('current-price', 'children')],
    [Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('stock-input', 'value')]
)
def update_graph_live(n_clicks, symbol):
    global submitted_tickers
    
    if n_clicks > 0:
        submitted_tickers.append(symbol)
    
    # Update graph
    fig = update_chart(symbol)
    
    # Get current price
    current_price = get_current_price(symbol)
    
    # Display ticker history
    history_text = "Submitted Tickers:\n" + "\n".join(submitted_tickers)
    
    return fig, history_text, f'Ticker Symbol: {symbol}', f'Current Price: ${current_price:.2f}'

if __name__ == '__main__':
    app.run_server(host='192.168.0.93', port=8050, debug=False)
