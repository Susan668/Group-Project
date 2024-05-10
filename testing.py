import streamlit as st, pandas as pd, numpy as np, yfinance as yf
import plotly.express as px

# Tab Title
st.set_page_config(page_title="BullBear", page_icon=":computer:")

from PIL import Image
logo = Image.open('logo.png')
st.image(logo)
# Title & Intro
with st.container():
  st.title("BullBear Stock Analysis:wave:")
  st.write("""
  Welcome to our BullBear Stock Analysis webpage for beginners! 
  Here's a simple webpage which you can easily track the returns of the technology stocks that you choose.
  """)


ticker = st.sidebar.selectbox("Ticker",
    ("MSFT", "GOOG", "AMZN", "NVDA","AAPL","META", "TSLA", "CRM", "AMD","BABA" ))
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")

data = yf.download(ticker,start=start_date, end=end_date)
fig = px.line(data, x = data.index, y = data['Adj Close'],title = ticker) #this is for the line-chart with a built in zoom feature
st.plotly_chart(fig)

pricing_data, fundamental_data, news = st.tabs(["Pricing Data", "Fundamental Data", "Top 5 News"])

with pricing_data:
    st.header("Price Movements")
    data2 = data
    data2["% Change"] = data["Adj Close"] / data["Adj Close"].shift(1) - 1
    data2.dropna(inplace = True)
    st.write(data2)
    annual_return = data2["% Change"].mean()*252*100
    st.write("Annual Return is", annual_return, "%")
    stdev = np.std(data2["% Change"])*np.sqrt(252) #the 252 days exclude all weakends
    st.write("Standard Deviation is", stdev*100, "%")
    st.write("Risk Adj. Return is", annual_return/(stdev*100))

from stocknews import StockNews
with news:
    st.header(f"News of {ticker}")
    sn = StockNews(ticker, save_news=False)
    df_news = sn.read_rss()
    for i in range(5):
        st.subheader(f"News {i+1}")
        st.write(df_news["published"][i])
        st.write(df_news["title"][i])
        st.write(df_news["summary"][i])
        

from alpha_vantage.fundamentaldata import FundamentalData
with fundamental_data:
    key = "U3TZCD5BHFMG8QLG"
    fd = FundamentalData(key, output_format = "pandas")
    st.subheader("Balance Sheet")
    balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
    bs = balance_sheet.T[2:]
    bs.columns = list(balance_sheet.T.iloc[0])
    st.write(bs)
    st.subheader("Income Statement")
    income_statement = fd.get_income_statement_annual(ticker)[0]
    is1 = income_statement.T[2:]
    is1.columns = list(income_statement.T.iloc[0])
    st.write(is1)
    st.subheader("Cash Flow Statement")
    cash_flow = fd.get_cash_flow_annual(ticker)[0]
    cf = cash_flow.T[2:]
    cf.columns = list(cash_flow.T.iloc[0])
    st.write(cf)
   