# Load Core Pkgs
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
from plotly.subplots import make_subplots
import datetime

# Function to fetch mutual fund data
def fetch_fund_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# Function to convert DataFrame to CSV for download
def convert_df_to_csv(df):
    return df.to_csv().encode('utf-8')

# Function to plot mutual fund data with returns and 20-day MA
def plot_fund_data(data, fund_name):
    fig = make_subplots(rows=2, cols=1, subplot_titles=(f'{fund_name} Price', f'{fund_name} Daily Return'),
                        vertical_spacing=0.2, row_heights=[0.6, 0.4])  # Adjust row heights

    # Plot raw data in the first subplot
    fig.add_trace(
        go.Scatter(x=data.index, y=data['Close'], mode='lines', name=f'{fund_name} Price'),
        row=1, col=1
    )

    # Calculate and plot 20-day moving average in the first subplot
    moving_average = data['Close'].rolling(window=20).mean()
    fig.add_trace(
        go.Scatter(x=data.index, y=moving_average, mode='lines', name=f'{fund_name} 20-Day MA', line=dict(dash='dot')),
        row=1, col=1
    )

    # Calculate and plot returns in the second subplot
    returns = data['Close'].pct_change()
    fig.add_trace(
        go.Scatter(x=data.index, y=returns, mode='lines', name=f'{fund_name} Daily Return'),
        row=2, col=1
    )

    fig.update_layout(
        title=f'{fund_name} Price and Returns',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        yaxis2_title='Daily Return',
        template='plotly_dark',
        height=800,
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="top",    # Anchor the legend at the top
            y=-0.1,           # Position below the plot
            xanchor="center", # Center the legend
            x=0.5             # Position at the middle
        )
    )

    return fig


def run_mutual_fund_app():
    # Mutual fund ticker to name mapping
    mutual_funds = {
        "VFINX": "Vanguard 500 Index Fund",
        "FXAIX": "Fidelity 500 Index Fund",
        "VTSMX": "Vanguard Total Stock Market Index Fund",
        "DODGX": "Dodge & Cox Stock Fund",
        "AGTHX": "American Funds Growth Fund of America",
        "TRBCX": "T. Rowe Price Blue Chip Growth Fund",
        "VGTSX": "Vanguard Total International Stock Index Fund",
        "PTTAX": "PIMCO Total Return Fund",
        "VBMFX": "Vanguard Total Bond Market Index Fund",
        "FKINX": "Franklin Income Fund"
    }

    # Sidebar for mutual fund selection
    fund_option = st.sidebar.selectbox('Select Mutual Fund', list(mutual_funds.values()))
    ticker = list(mutual_funds.keys())[list(mutual_funds.values()).index(fund_option)]

    # Sidebar for date range selection
    start_date = pd.Timestamp(st.sidebar.date_input('Start Date', datetime.date(2023, 1, 1)))
    end_date = pd.Timestamp(st.sidebar.date_input('End Date', datetime.date.today()))

    if start_date > end_date:
        st.sidebar.error("End date must be after start date.")

    # Fetching mutual fund data
    data = fetch_fund_data(ticker, start_date, end_date)

    # Streamlit interface
    st.subheader(f"{fund_option} Fund Data")
    
    # Data preview
    data_exp = st.expander("Preview Data")
    data_exp.dataframe(data)

    # Download button for data
    csv_file = convert_df_to_csv(data)
    data_exp.download_button(
        label="Download Data as CSV",
        data=csv_file,
        file_name=f"{fund_option}_data.csv",
        mime="text/csv",
    )

    # Plotting the data
    fig = plot_fund_data(data, fund_option)
    st.plotly_chart(fig)


