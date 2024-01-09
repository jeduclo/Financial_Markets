# Load Core Pkgs
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
from plotly.subplots import make_subplots
import datetime

# Function to fetch currency exchange rate data
def fetch_currency_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# Function to convert DataFrame to CSV for download
def convert_df_to_csv(df):
    return df.to_csv().encode('utf-8')

# Function to plot currency exchange rate data with returns and 20-day MA
def plot_currency_data(data, currency_name):
    fig = make_subplots(rows=2, cols=1, subplot_titles=(f'{currency_name} Exchange Rate', f'{currency_name} Daily Return'),
                        vertical_spacing=0.2, row_heights=[0.6, 0.4])

    # Plot raw data in the first subplot
    fig.add_trace(
        go.Scatter(x=data.index, y=data['Close'], mode='lines', name=f'{currency_name} Rate'),
        row=1, col=1
    )

    # Calculate and plot 20-day moving average in the first subplot
    moving_average = data['Close'].rolling(window=20).mean()
    fig.add_trace(
        go.Scatter(x=data.index, y=moving_average, mode='lines', name=f'{currency_name} 20-Day MA', line=dict(dash='dot')),
        row=1, col=1
    )

    # Calculate and plot returns in the second subplot
    returns = data['Close'].pct_change()
    fig.add_trace(
        go.Scatter(x=data.index, y=returns, mode='lines', name=f'{currency_name} Daily Return'),
        row=2, col=1
    )

    fig.update_layout(
        title=f'{currency_name} Exchange Rate and Returns',
        xaxis_title='Date',
        yaxis_title='Exchange Rate',
        yaxis2_title='Daily Return',
        template='plotly_dark',
        height=800,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.1,
            xanchor="center",
            x=0.5
        )
    )

    return fig

def run_currency_app():
    # Currency ticker to name mapping
    currency_tickers = {
        "CADUSD=X": "CAD/USD", "CADEUR=X": "CAD/EUR", "CADJPY=X": "CAD/JPY", "CADGBP=X": "CAD/GBP",
        "CADAUD=X": "CAD/AUD", "CADCHF=X": "CAD/CHF", "CADNZD=X": "CAD/NZD", "CADCNY=X": "CAD/CNY",
        "CADSEK=X": "CAD/SEK", "CADNOK=X": "CAD/NOK"
    }

    # Sidebar for currency selection
    currency_option = st.sidebar.selectbox('Select Currency Pair', list(currency_tickers.values()))
    ticker = list(currency_tickers.keys())[list(currency_tickers.values()).index(currency_option)]

    # Sidebar for date range selection
    start_date = pd.Timestamp(st.sidebar.date_input('Start Date', datetime.date(2020, 1, 1)))
    end_date = pd.Timestamp(st.sidebar.date_input('End Date', datetime.date.today()))

    if start_date > end_date:
        st.sidebar.error("End date must be after start date.")

    # Fetching currency data
    data = fetch_currency_data(ticker, start_date, end_date)

    # Streamlit interface
    st.subheader(f"{currency_option} Exchange Rate Data")
    
    # Data preview
    data_exp = st.expander("Preview Data")
    data_exp.dataframe(data)

    # Download button for data
    csv_file = convert_df_to_csv(data)
    data_exp.download_button(
        label="Download Data as CSV",
        data=csv_file,
        file_name=f"{currency_option}_exchange_rate.csv",
        mime="text/csv",
    )

    # Plotting the data
    fig = plot_currency_data(data, currency_option)
    st.plotly_chart(fig)


