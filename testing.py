import streamlit as st, pandas as pd, numpy as np, yfinance as yf
import plotly.express as px

# Reference of the codes for our group project: Dashora.R. [Financial Programming with Ritvik, CFA]. (2022, December 25). Streamlit STOCK dashboard using Python. [Video]. YouTube. https://youtu.be/fdFfpEtv5BU?si=AqqZLsS0OtXckGub

# Setting Tab Title
st.set_page_config(page_title="BullBear", page_icon=":computer:")

# Adding the logo to the web application, the logo is created by ourselves
from PIL import Image
logo = Image.open('logo.png')
st.image(logo)

# Adding the title and introduction to the web application
with st.container():
  st.title("BullBear Stock Analysis:wave:")
  st.write("""
  Welcome to our BullBear Stock Analysis webpage for beginners! 
  Here's a simple webpage which you can easily track the returns of the technology stocks that you choose.
  """)

# Creating the dropdown menu of ten trendy technology stocks, and the dates for the users to select 
ticker = st.sidebar.selectbox("Ticker",
    ("MSFT", "GOOG", "AMZN", "NVDA","AAPL","META", "TSLA", "CRM", "AMD","BABA" ))
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")

# Retrieving the data from yfinance
try:
  data = yf.download(ticker,start=start_date, end=end_date)
  if data.empty:
      print("No data found for the specified range and ticker.")
  else:
       print(data)
except Exception as e:
  print(f"Failed to download data: {e}")

# Plotting the graph to see the movements of Adjusted Close (Adj close)
# Adjusted Close is the closing price after adjustments for all applicable splits and dividend distributions.
fig = px.line(data, x = data.index, y = data['Adj Close'],title = ticker) #this is for the line-chart with a built in zoom feature
st.plotly_chart(fig)

pricing_data, news = st.tabs(["Pricing Data", "Top 5 News"])

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
        


   
