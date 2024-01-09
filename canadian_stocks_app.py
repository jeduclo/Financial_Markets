# Load Core Pkgs
import yfinance as yf
import streamlit as st
import datetime 
import pandas as pd
import cufflinks as cf
from plotly.offline import iplot

def run_canadian_stocks_app():
    # st.subheader("From stock")
    ## set offline mode for cufflinks
    cf.go_offline()

    # data functions
    #@st.cache_data
    def get_tsx_components():
        df = pd.read_html("https://en.wikipedia.org/wiki/S%26P/TSX_Composite_Index")
        df = df[1]
        tickers = df["Ticker"].to_list()
        tickers_companies_dict = dict(
            zip(df["Ticker"], df["Company"])
        )
        return tickers, tickers_companies_dict

    #@st.cache_data
    def load_data(symbol, start, end):
        return yf.download(symbol, start, end)

    #@st.cache_data
    def convert_df_to_csv(df):
        return df.to_csv().encode("utf-8")

    # sidebar

    ## inputs for downloading data
    st.sidebar.header("Stock Parameters")

    available_tickers, tickers_companies_dict = get_tsx_components()

    ticker = st.sidebar.selectbox(
        "Ticker", 
        available_tickers, 
        format_func=tickers_companies_dict.get
    )
    start_date = st.sidebar.date_input(
        "Start date", 
        datetime.date(2017, 1, 1)
    )
    end_date = st.sidebar.date_input(
        "End date", 
        datetime.date.today()
    )

    if start_date > end_date:
        st.sidebar.error("The end date must fall after the start date")

    ## inputs for technical analysis
    st.sidebar.header("Technical Analysis Parameters")

    volume_flag = st.sidebar.checkbox(label="Add volume")

    exp_sma = st.sidebar.expander("SMA")
    sma_flag = exp_sma.checkbox(label="Add SMA")
    sma_periods= exp_sma.number_input(
        label="SMA Periods", 
        min_value=1, 
        max_value=50, 
        value=20, 
        step=1
    )

    exp_bb = st.sidebar.expander("Bollinger Bands")
    bb_flag = exp_bb.checkbox(label="Add Bollinger Bands")
    bb_periods= exp_bb.number_input(label="BB Periods", 
                                    min_value=1, max_value=50, 
                                    value=20, step=1)
    bb_std= exp_bb.number_input(label="# of standard deviations", 
                                min_value=1, max_value=4, 
                                value=2, step=1)

    exp_rsi = st.sidebar.expander("Relative Strength Index")
    rsi_flag = exp_rsi.checkbox(label="Add RSI")
    rsi_periods= exp_rsi.number_input(
        label="RSI Periods", 
        min_value=1, 
        max_value=50, 
        value=20, 
        step=1
    )
    rsi_upper= exp_rsi.number_input(label="RSI Upper", 
                                    min_value=50, 
                                    max_value=90, value=70, 
                                    step=1)
    rsi_lower= exp_rsi.number_input(label="RSI Lower", 
                                    min_value=10, 
                                    max_value=50, value=30, 
                                    step=1)

    # main body

    st.subheader("Unveiling Economic Insights Through the Visualization of Toronto TSX Data")
    st.write("""
    ### Background
    The Toronto Stock Exchange (TSX) stands as the largest stock exchange in Canada 
    and the third largest in North America. The TSX serves as a temperature check 
    for Canada's economic health, hosting a wide range of sectors and businesses. 
    Visualizing data from the TSX provides a compelling 
    and effective means of deciphering complex economic patterns and trends.

    **Sectoral Comparison:** Visual representation of TSX data simplifies the comparison of 
    performance across different industries and sectors. Such comparisons can help identify 
    which sectors are propelling economic 
    growth at any given moment and which are facing challenges.
    
    **Insights into Economic Performance:** TSX hosts a diverse array of companies 
    across various sectors of the economy. Hence, trends in these stocks often 
    mirror the overall performance of the economy. Visualizing this data provides 
    invaluable insights into various economic 
    indicators such as employment rate, consumer spending, investment trends, and more.


    """)

    df = load_data(ticker, start_date, end_date)

    ## data preview part
    data_exp = st.expander("Preview data")
    available_cols = df.columns.tolist()
    columns_to_show = data_exp.multiselect(
        "Columns", 
        available_cols, 
        default=available_cols
    )
    data_exp.dataframe(df[columns_to_show])

    csv_file = convert_df_to_csv(df[columns_to_show])
    data_exp.download_button(
        label="Download selected as CSV",
        data=csv_file,
        file_name=f"{ticker}_stock_prices.csv",
        mime="text/csv",
    )

    ## technical analysis plot
    title_str = f"{tickers_companies_dict[ticker]}'s stock price"
    qf = cf.QuantFig(df, title=title_str)
    if volume_flag:
        qf.add_volume()
    if sma_flag:
        qf.add_sma(periods=sma_periods)
    if bb_flag:
        qf.add_bollinger_bands(periods=bb_periods,
                            boll_std=bb_std)
    if rsi_flag:
        qf.add_rsi(periods=rsi_periods,
                rsi_upper=rsi_upper,
                rsi_lower=rsi_lower,
                showbands=True)

    fig = qf.iplot(asFigure=True)
    st.plotly_chart(fig)






