# Core pkgs
import streamlit as st

# Import Mini Apps
from market_index_app import run_market_indices_app
from crypto_app import run_crypto_app
from currency_app import run_currency_app
from top_etf_app import run_etf_app
from top_mutual_fund_app import run_mutual_fund_app
from treasury_yields_app import run_treasury_yields_app
from economic_sectors_app import run_sector_etfs_app
from canadian_stocks_app import run_canadian_stocks_app
from sp500_app import run_sp500_app
from top_bond_etf_app import run_bond_etfs_app
from commodities_app import run_commodities_app

def run_home_app():
    st.title("Welcome to the Financial Market Insights App")
    st.write("""
    This application provides a comprehensive overview of major financial markets and indicators. 
    You can explore various aspects like market indexes, cryptocurrencies, currencies, ETFs, mutual funds, 
    treasury yields, economic sectors, Canadian stocks, S&P 500, bond ETFs, and commodities. 
    You are also able to download the data.

    Please select a category from the sidebar to explore further.
    """)

def main():
    menu = ["Home", "Market Index", "Cryptocurrencies", "Currencies", "Top ETFs", 
            "Top Mutual Funds", "Treasury Yields", "Economic Sectors", "Canadian Stocks", 
            "S&P 500", "Top Bond ETFs", "Commodities"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        run_home_app()
    elif choice == "Market Index":
        run_market_indices_app()
    elif choice == "Cryptocurrencies":
        run_crypto_app()
    elif choice == "Currencies":
        run_currency_app()
    elif choice == "Top ETFs":
        run_etf_app()
    elif choice == "Top Mutual Funds":
        run_mutual_fund_app()
    elif choice == "Treasury Yields":
        run_treasury_yields_app()
    elif choice == "Economic Sectors":
        run_sector_etfs_app()
    elif choice == "Canadian Stocks":
        run_canadian_stocks_app()
    elif choice == "S&P 500":
        run_sp500_app()
    elif choice == "Top Bond ETFs":
        run_bond_etfs_app()
    elif choice == "Commodities":
        run_commodities_app()

if __name__ == '__main__':
    main()
