# Load Core Pkgs
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
from plotly.subplots import make_subplots
import datetime

# Function to fetch sector ETF data
def fetch_sector_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# Function to convert DataFrame to CSV for download
def convert_df_to_csv(df):
    return df.to_csv().encode('utf-8')

# Function to plot sector ETF data with returns and 20-day MA
def plot_sector_data(data, sector_name):
    fig = make_subplots(rows=2, cols=1, subplot_titles=(f'{sector_name}', f'{sector_name} Daily Return'),
                        vertical_spacing=0.2, row_heights=[0.6, 0.4])

    # Plot raw data in the first subplot
    fig.add_trace(
        go.Scatter(x=data.index, y=data['Close'], mode='lines', name=f'{sector_name} Price'),
        row=1, col=1
    )

    # Calculate and plot 20-day moving average in the first subplot
    moving_average = data['Close'].rolling(window=20).mean()
    fig.add_trace(
        go.Scatter(x=data.index, y=moving_average, mode='lines', name=f'{sector_name} 20-Day MA', line=dict(dash='dot')),
        row=1, col=1
    )

    # Calculate and plot returns in the second subplot
    returns = data['Close'].pct_change()
    fig.add_trace(
        go.Scatter(x=data.index, y=returns, mode='lines', name=f'{sector_name} Daily Return'),
        row=2, col=1
    )

    fig.update_layout(
        title=f'{sector_name} Price and Returns',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
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

def run_sector_etfs_app():
    # Sector ETF ticker to name mapping
    sector_etfs = {
        "XLK": "Technology",
        "XLV": "Healthcare",
        "XLF": "Financials",
        "XLY": "Consumer Discretionary",
        "XLP": "Consumer Staples",
        "XLE": "Energy",
        "XLI": "Industrials",
        "XLB": "Materials",
        "XLU": "Utilities",
        "XLRE": "Real Estate"
    }

    # Sidebar for sector ETF selection
    sector_option = st.sidebar.selectbox('Select Sector ETF', list(sector_etfs.values()))
    ticker = list(sector_etfs.keys())[list(sector_etfs.values()).index(sector_option)]

    # Sidebar for date range selection
    start_date = pd.Timestamp(st.sidebar.date_input('Start Date', datetime.date(2020, 1, 1)))
    end_date = pd.Timestamp(st.sidebar.date_input('End Date', datetime.date.today()))

    if start_date > end_date:
        st.sidebar.error("End date must be after start date.")

    # Fetching sector ETF data
    data = fetch_sector_data(ticker, start_date, end_date)

    # Streamlit interface
    st.subheader(f"{sector_option} Sector ETF Data")
    
    # Data preview
    data_exp = st.expander("Preview Data")
    data_exp.dataframe(data)

    # Download button for data
    csv_file = convert_df_to_csv(data)
    data_exp.download_button(
        label="Download Data as CSV",
        data=csv_file,
        file_name=f"{sector_option}_data.csv",
        mime="text/csv",
    )

    # Plotting the data
    fig = plot_sector_data(data, sector_option)
    st.plotly_chart(fig)


