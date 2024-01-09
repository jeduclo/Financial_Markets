# Load Core Pkgs
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
from plotly.subplots import make_subplots
import datetime

# Function to fetch market index data
def fetch_index_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# Function to convert DataFrame to CSV for download
def convert_df_to_csv(df):
    return df.to_csv().encode('utf-8')

# Function to plot market index data with returns and 20-day MA
def plot_index_data(data, index_name):
    fig = make_subplots(rows=2, cols=1, subplot_titles=(f'{index_name}', f'{index_name} Daily Return'),
                        vertical_spacing=0.2, row_heights=[0.6, 0.4])

    # Plot raw data in the first subplot
    fig.add_trace(
        go.Scatter(x=data.index, y=data['Close'], mode='lines', name=f'{index_name} Value'),
        row=1, col=1
    )

    # Calculate and plot 20-day moving average in the first subplot
    moving_average = data['Close'].rolling(window=20).mean()
    fig.add_trace(
        go.Scatter(x=data.index, y=moving_average, mode='lines', name=f'{index_name} 20-Day MA', line=dict(dash='dot')),
        row=1, col=1
    )

    # Calculate and plot returns in the second subplot
    returns = data['Close'].pct_change()
    fig.add_trace(
        go.Scatter(x=data.index, y=returns, mode='lines', name=f'{index_name} Daily Return'),
        row=2, col=1
    )

    fig.update_layout(
        title=f'{index_name} Value and Returns',
        xaxis_title='Date',
        yaxis_title='Index Value',
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

def run_market_indices_app():
    # Market indices ticker to name mapping
    indices = {
        "^DJI": "Dow Jones Industrial Average",
        "^GSPC": "S&P 500",
        "^IXIC": "NASDAQ Composite",
        "^FTSE": "FTSE 100",
        "^GDAXI": "DAX",
        "^FCHI": "CAC 40",
        "^N225": "Nikkei 225",
        "^HSI": "Hang Seng Index",
        "^SSEC": "Shanghai Composite",
        "^AXJO": "S&P/ASX 200"
    }

    # Sidebar for market index selection
    index_option = st.sidebar.selectbox('Select Market Index', list(indices.values()))
    ticker = list(indices.keys())[list(indices.values()).index(index_option)]

    # Sidebar for date range selection
    start_date = st.sidebar.date_input('Start Date', datetime.date(2020, 1, 1))
    end_date = st.sidebar.date_input('End Date', datetime.date.today())

    if start_date > end_date:
        st.sidebar.error("End date must be after start date.")
        st.stop()
    elif start_date == end_date:
        st.sidebar.warning("Start date and end date are the same. Data might be limited.")
    
    # Fetching market index data
    data = fetch_index_data(ticker, pd.Timestamp(start_date), pd.Timestamp(end_date))

    # Streamlit interface
    st.subheader(f"{index_option} Market Index Data")
    
    # Data preview
    data_exp = st.expander("Preview Data")
    data_exp.dataframe(data)

    # Download button for data
    csv_file = convert_df_to_csv(data)
    data_exp.download_button(
        label="Download Data as CSV",
        data=csv_file,
        file_name=f"{index_option}_market_index_data.csv",
        mime="text/csv",
    )

    # Plotting the data
    fig = plot_index_data(data, index_option)
    st.plotly_chart(fig)


