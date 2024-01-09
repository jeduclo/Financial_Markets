# Load Core Pkgs
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import plotly.subplots as sp
import pandas as pd
import datetime 





def run_commodities_app():
    # Ticker to commodity name mapping
    ticker_to_name = {
        "CL=F": "Crude Oil",
        "BZ=F":"Brent Crude",
        "HO=F":"Heating Oil",
        "RB=F":"Gasoline",
        "NG=F": "Natural Gas",
        "GC=F": "Gold",
        "SI=F": "Silver",
        "HG=F": "Copper",
        "PL=F": "Platinum",
        "PA=F":"Palladium",
        "ZC=F":"Corn",
        "ZS=F":"Soybeans",
        "LBS=F": "Lumber",
        "CT=F":"Cotton",
        "SB=F":"Sugar",
        "KC=F":"Coffee",
        "LE=F":"Live Cattle",
        "GF=F":"Feeder Cattle",
        "HE=F":"Lean Hogs",
        "DBA": "Agriculture",
        "ZW=F": "Wheat",
        "NTR": "Potash (Nutrien Ltd.)",
        "URA": "Uranium",
        "ALI=F":"Aluminum"
    }

    

    commodity_option = st.sidebar.selectbox('Select commodity', list(ticker_to_name.values()))
    ticker = list(ticker_to_name.keys())[list(ticker_to_name.values()).index(commodity_option)]

    start_date = pd.Timestamp(st.sidebar.date_input('Start date', datetime.date(2021, 1, 1)))
    end_date = pd.Timestamp(st.sidebar.date_input('End date', datetime.date.today()))


    if start_date > end_date:
        st.sidebar.error("The end date must fall after the start date.")



    # import and clean Data
    #@st.cache_data
    def fetch_commodity_data(ticker, start_date, end_date):
        data = yf.download(ticker, start=start_date, end=end_date)
        return data

    data = fetch_commodity_data(ticker, start_date, end_date)
    
    
    #@st.cache_data
    def convert_df_to_csv(df):
        return df.to_csv().encode("utf-8")
    

    def plot_data(data, commodity_name):
        fig = sp.make_subplots(rows=2, cols=1)

        # Plot raw data
        fig.add_trace(
            go.Scatter(x=data.index, y=data['Close'], name=commodity_name),
            row=1, col=1
        )

        # Calculate and plot 20-day moving average
        moving_average = data['Close'].rolling(window=20).mean()
        fig.add_trace(
            go.Scatter(x=data.index, y=moving_average, name=commodity_name + " 20-Day MA", line=dict(dash='dot')),
            row=1, col=1
        )

        # Calculate and plot returns
        fig.add_trace(
            go.Scatter(
                x=data.index, 
                y=data['Close'].pct_change(), 
                name=commodity_name + " Returns",
                line=dict(color='#275782', width=2)  # Set the color to light green
            ),
            row=2, col=1
        )


        fig.update_layout(
            height=800,  # This makes the plot adjust to the size of the browser window
            title_text='Commodity Prices Over Time: '+commodity_name,
            title_font_size=14,
            title_y=0.95,
            legend=dict(x=0.6, y=1.1)  # Update position of legend
        )

        fig.update_yaxes(title_text="Price", row=1, col=1)
        fig.update_yaxes(title_text="Returns", row=2, col=1)

        return fig

        # Streamlit code
    st.subheader("Commodities Futures")
    

    data_exp = st.expander("Preview Commodity Data")
    data_exp.dataframe(data)

    csv_file = convert_df_to_csv(data)
    data_exp.download_button(
        label="Download selected as CSV",
        data=csv_file,
        file_name="commodities_data.csv",
        mime="text/csv",
    )


    fig = plot_data(data, commodity_option)
    st.plotly_chart(fig)
    






