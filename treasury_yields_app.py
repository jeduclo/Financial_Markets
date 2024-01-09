# Load Core Pkgs
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
from plotly.subplots import make_subplots
import datetime

# Function to fetch Treasury yield data
def fetch_yield_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# Function to convert DataFrame to CSV for download
def convert_df_to_csv(df):
    return df.to_csv().encode('utf-8')

# Function to plot Treasury yield data with returns and 20-day MA
def plot_yield_data(data, yield_name):
    fig = make_subplots(rows=2, cols=1, subplot_titles=(f'{yield_name}', f'{yield_name} Daily Return'),
                        vertical_spacing=0.2, row_heights=[0.6, 0.4])

    # Plot raw data in the first subplot
    fig.add_trace(
        go.Scatter(x=data.index, y=data['Close'], mode='lines', name=f'{yield_name} Yield'),
        row=1, col=1
    )

    # Calculate and plot 20-day moving average in the first subplot
    moving_average = data['Close'].rolling(window=20).mean()
    fig.add_trace(
        go.Scatter(x=data.index, y=moving_average, mode='lines', name=f'{yield_name} 20-Day MA', line=dict(dash='dot')),
        row=1, col=1
    )

    # Calculate and plot returns in the second subplot
    returns = data['Close'].pct_change()
    fig.add_trace(
        go.Scatter(x=data.index, y=returns, mode='lines', name=f'{yield_name} Daily Return'),
        row=2, col=1
    )

    fig.update_layout(
        title=f'{yield_name} Yield and Returns',
        xaxis_title='Date',
        yaxis_title='Yield (%)',
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

def run_treasury_yields_app():
    # Treasury yields ticker to name mapping
    treasury_yields = {
        "^IRX": "13-Week Treasury Bill",
        "^FVX": "5-Year Treasury Note",
        "^TNX": "CBOE 10-Year Treasury Note",
        "^TYX": "30-Year Treasury Bond"
    }

    # Sidebar for Treasury yield selection
    yield_option = st.sidebar.selectbox('Select Treasury Yield', list(treasury_yields.values()))
    ticker = list(treasury_yields.keys())[list(treasury_yields.values()).index(yield_option)]

    # Sidebar for date range selection
    start_date = pd.Timestamp(st.sidebar.date_input('Start Date', datetime.date(2023, 1, 1)))
    end_date = pd.Timestamp(st.sidebar.date_input('End Date', datetime.date.today()))

    if start_date > end_date:
        st.sidebar.error("End date must be after start date.")

    # Fetching Treasury yield data
    data = fetch_yield_data(ticker, start_date, end_date)

    # Streamlit interface
    st.subheader(f"{yield_option} Treasury Yield Data")
    
    # Data preview
    data_exp = st.expander("Preview Data")
    data_exp.dataframe(data)

    # Download button for data
    csv_file = convert_df_to_csv(data)
    data_exp.download_button(
        label="Download Data as CSV",
        data=csv_file,
        file_name=f"{yield_option}_data.csv",
        mime="text/csv",
    )

    # Plotting the data
    fig = plot_yield_data(data, yield_option)
    st.plotly_chart(fig)


