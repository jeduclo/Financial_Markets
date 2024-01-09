# Load Core Pkgs
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
import datetime
# Import make_subplots
from plotly.subplots import make_subplots


# Function to fetch cryptocurrency data
def fetch_crypto_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# Function to convert DataFrame to CSV for download
def convert_df_to_csv(df):
    return df.to_csv().encode('utf-8')

# Function to plot cryptocurrency data with returns and 20-day MA
def plot_crypto_data(data, crypto_name):
    # Create subplots: one for price and moving average, another for returns
    fig = make_subplots(rows=2, cols=1, subplot_titles=(f'{crypto_name} Price', f'{crypto_name} Daily Return'),
                        vertical_spacing=0.2)

    # Plot raw data in the first subplot
    fig.add_trace(
        go.Scatter(x=data.index, y=data['Close'], mode='lines', name=f'{crypto_name} Price'),
        row=1, col=1
    )

    # Calculate and plot 20-day moving average in the first subplot
    moving_average = data['Close'].rolling(window=20).mean()
    fig.add_trace(
        go.Scatter(x=data.index, y=moving_average, mode='lines', name=f'{crypto_name} 20-Day MA', line=dict(dash='dot')),
        row=1, col=1
    )

    # Calculate and plot returns in the second subplot
    returns = data['Close'].pct_change()
    fig.add_trace(
        go.Scatter(x=data.index, y=returns, mode='lines', name=f'{crypto_name} Daily Return'),
        row=2, col=1
    )

    # Update layout
    fig.update_layout(
        title=f'{crypto_name} Price and Returns',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        yaxis2_title='Daily Return',
        template='plotly_dark',
        height=800
    )

    return fig



def run_crypto_app():
    # Cryptocurrency ticker to name mapping
    cryptos = {
        "BTC-USD": "Bitcoin",
        "ETH-USD": "Ethereum",
        "BNB-USD": "Binance Coin",
        "ADA-USD": "Cardano",
        "XRP-USD": "Ripple",
        "SOL-USD": "Solana",
        "DOT-USD": "Polkadot",
        "LTC-USD": "Litecoin",
        "LINK-USD": "Chainlink",
        "BCH-USD": "Bitcoin Cash"
    }

    # Sidebar for cryptocurrency selection
    crypto_option = st.sidebar.selectbox('Select Cryptocurrency', list(cryptos.values()))
    ticker = list(cryptos.keys())[list(cryptos.values()).index(crypto_option)]

    # Sidebar for date range selection
    start_date = pd.Timestamp(st.sidebar.date_input('Start Date', datetime.date(2023, 1, 1)))
    end_date = pd.Timestamp(st.sidebar.date_input('End Date', datetime.date.today()))

    if start_date > end_date:
        st.sidebar.error("End date must be after start date.")

    # Fetching cryptocurrency data
    data = fetch_crypto_data(ticker, start_date, end_date)

    # Streamlit interface
    st.subheader(f"{crypto_option} Price Data")
    
    # Data preview
    data_exp = st.expander("Preview Data")
    data_exp.dataframe(data)

    # Download button for data
    csv_file = convert_df_to_csv(data)
    data_exp.download_button(
        label="Download Data as CSV",
        data=csv_file,
        file_name=f"{crypto_option}_data.csv",
        mime="text/csv",
    )

    # Plotting the data
    fig = plot_crypto_data(data, crypto_option)
    st.plotly_chart(fig)

if __name__ == '__main__':
    run_crypto_app()
