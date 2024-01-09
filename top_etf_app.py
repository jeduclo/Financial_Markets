# Load Core Pkgs
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
from plotly.subplots import make_subplots
import datetime

# Function to fetch ETF data
def fetch_etf_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# Function to convert DataFrame to CSV for download
def convert_df_to_csv(df):
    return df.to_csv().encode('utf-8')

# Function to plot ETF data with returns and 20-day MA
def plot_etf_data(data, etf_name):
    fig = make_subplots(rows=2, cols=1, subplot_titles=(f'{etf_name}', f'{etf_name} Daily Return'),
                        vertical_spacing=0.2, row_heights=[0.6, 0.4])

    # Plot raw data in the first subplot
    fig.add_trace(
        go.Scatter(x=data.index, y=data['Close'], mode='lines', name=f'{etf_name} Price'),
        row=1, col=1
    )

    # Calculate and plot 20-day moving average in the first subplot
    moving_average = data['Close'].rolling(window=20).mean()
    fig.add_trace(
        go.Scatter(x=data.index, y=moving_average, mode='lines', name=f'{etf_name} 20-Day MA', line=dict(dash='dot')),
        row=1, col=1
    )

    # Calculate and plot returns in the second subplot
    returns = data['Close'].pct_change()
    fig.add_trace(
        go.Scatter(x=data.index, y=returns, mode='lines', name=f'{etf_name} Daily Return'),
        row=2, col=1
    )

    fig.update_layout(
        title=f'{etf_name} Price and Returns',
        xaxis_title='Date',
        yaxis_title='ETF Price',
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

def run_etf_app():
    # ETF ticker to name mapping
    etfs = {
        "SPY": "SPDR S&P 500 ETF Trust",
        "IVV": "iShares Core S&P 500 ETF",
        "VTI": "Vanguard Total Stock Market ETF",
        "QQQ": "Invesco QQQ Trust",
        "VOO": "Vanguard S&P 500 ETF",
        "IWM": "iShares Russell 2000 ETF",
        "VWO": "Vanguard FTSE Emerging Markets ETF",
        "EFA": "iShares MSCI EAFE ETF",
        "AGG": "iShares Core U.S. Aggregate Bond ETF",
        "BND": "Vanguard Total Bond Market ETF"
    }

    # Sidebar for ETF selection
    etf_option = st.sidebar.selectbox('Select ETF', list(etfs.values()))
    ticker = list(etfs.keys())[list(etfs.values()).index(etf_option)]

    # Sidebar for date range selection
    start_date = pd.Timestamp(st.sidebar.date_input('Start Date', datetime.date(2020, 1, 1)))
    end_date = pd.Timestamp(st.sidebar.date_input('End Date', datetime.date.today()))

    if start_date > end_date:
        st.sidebar.error("End date must be after start date.")

    # Fetching ETF data
    data = fetch_etf_data(ticker, start_date, end_date)

    # Streamlit interface
    st.subheader(f"{etf_option} ETF Data")
    
    # Data preview
    data_exp = st.expander("Preview Data")
    data_exp.dataframe(data)

    # Download button for data
    csv_file = convert_df_to_csv(data)
    data_exp.download_button(
        label="Download Data as CSV",
        data=csv_file,
        file_name=f"{etf_option}_data.csv",
        mime="text/csv",
    )

    # Plotting the data
    fig = plot_etf_data(data, etf_option)
    st.plotly_chart(fig)

