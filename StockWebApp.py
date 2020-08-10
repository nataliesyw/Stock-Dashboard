# Description : This is a stock market dashboard to show some stocks and charts
import streamlit as st
import pandas as pd
from PIL import Image

# Add a title and an image
st.write("""
# Stock Market Web Application 
**Visually** show data on a stock
Date range from Jan 2, 2020 to 4 Jul 4, 2020
""")

image = Image.open("/Users/natalie/PycharmProjects/Stock/venv/stock-market-coronavirus-2.jpg")
st.image(image, use_column_width=True)

# Create a sidebar
st.sidebar.header('User Input')


def get_input():
    start_date = st.sidebar.text_input("Start Date", "2020-01-02")
    end_date = st.sidebar.text_input("End Date", "2020-07-04")
    stock_symbol = st.sidebar.text_input("Stock Symbol", "AMZN")
    return start_date, end_date, stock_symbol


def get_company_name(stock):
    if stock == 'AMZN':
        return 'Amazon'
    elif stock == 'TSLA':
        return 'Tesla'
    elif stock == 'GOOG':
        return 'Alphabet'
    else:
        'None'


# get the proper company name and timeframe from the user input
def get_data(stock_symbol, start_date, end_date):
    # load the data
    if stock_symbol.upper() == 'AMZN':
        dataf = pd.read_csv("/Users/natalie/PycharmProjects/Stock/Stocks/AMZN.csv")
    elif stock_symbol.upper() == 'GOOG':
        dataf = pd.read_csv("/Users/natalie/PycharmProjects/Stock/Stocks/GOOG.csv")
    elif stock_symbol.upper() == 'TSLA':
        dataf = pd.read_csv("/Users/natalie/PycharmProjects/Stock/Stocks/TSLA.csv")
    else:
        dataf = pd.DataFrame(columns=['Date', 'Close', 'Open', 'Volume', 'Adj Close', 'High', 'Low'])

    # get the date range
    start_date = pd.to_datetime(start_date, errors='coerce')
    end_date = pd.to_datetime(end_date, errors='coerce')

    # set the start and end index row to 0
    start_row = 0
    end_row = 0

    for i in range(0, len(dataf)):
        if start_date <= pd.to_datetime(dataf['Date'][i], errors='coerce'):
            start_row = i
            break

    for j in range(0, len(dataf)):
        if start_date >= pd.to_datetime(dataf['Date'][len(dataf) - 1 - j], errors='coerce'):
            end_row = len(dataf) - 1 - j
            break

    # set the index to be the date
    dataf.set_index(pd.DatetimeIndex(dataf['Date'].values))

    return dataf.iloc[start_row: end_row + 1, :]


start, end, symbol = get_input()
df = get_data(start, end, symbol)
company_name = get_company_name(symbol.upper())

# display close price
st.header(company_name+" Close Price\n")
st.line_chart(df['Close'])

# display volume
st.header(company_name+" Volume\n")
st.line_chart(df['Volume'])

# Get Statistics from data
st.header('Data Statistics')
st.write(df.descrbe())
