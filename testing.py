import streamlit as st, pandas as pd, numpy as np, yfinance as yf
import plotly.express as px

# Reference of the codes starting from line 23 to the end: Dashora.R. [Financial Programming with Ritvik, CFA]. (2022, December 25). Streamlit STOCK dashboard using Python. [Video]. YouTube. https://youtu.be/fdFfpEtv5BU?si=AqqZLsS0OtXckGub

# Tab-Titel festlegen
st.set_page_config(page_title="BullBear", page_icon=":computer:")

# Hinzufügen des Logos zur Webanwendung, das Logo wird von uns selbst erstellt
from PIL import Image
logo = Image.open('logo.png')
st.image(logo)

# Hinzufügen des Titels und der Einleitung zur Webanwendung
with st.container():
  st.title("BullBear Stock Analysis:wave:")
  st.write("""
  Welcome to our BullBear Stock Analysis webpage for beginners! 
  Here's a simple webpage which you can easily track the returns of the technology stocks that you choose.
  """)

# Erstellung eines Dropdown-Menüs mit zehn Technologiewerten und den Daten, die die Benutzer auswählen können 
ticker = st.sidebar.selectbox("Ticker",
    ("MSFT", "GOOG", "AMZN", "NVDA","AAPL","META", "TSLA", "CRM", "AMD","BABA" ))
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")

# Abrufen der Daten aus yfinance und Testen, ob die Daten erfolgreich geladen werden können
try:
  data = yf.download(ticker,start=start_date, end=end_date)
  if data.empty:
      print("No data found for the specified range and ticker.")
  else:
       print(data)
except Exception as e:
  print(f"Failed to download data: {e}")

# Darstellung des Diagramms, um die Bewegungen des Adjusted Close (Adj close) zu sehen
fig = px.line(data, x = data.index, y = data['Adj Close'],title = ticker) #this is for the line-chart with a built in zoom feature
st.plotly_chart(fig)

# Erstellen der Registerkarten für Pricing Data und Top 5 News
pricing_data, news = st.tabs(["Pricing Data", "Top 5 News"])

# Erstellen Sie für Pricing Data die Tabellen mit den Preisbewegungen (price movements), der jährlichen Rendite (annual return), der Standardabweichung (standard deviation) und der zusätzlichen Rendite von Rick (rick adj. return).
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

# Abrufen von Daten für die Nachrichten von Aktien 
from stocknews import StockNews

#Anzeige der 5 wichtigsten Nachrichten mit Veröffentlichungsdaten, Titeln, Zusammenfassungen, Titelstimmungen (title sentiment) und Nachrichtenempfindungen (news sentiment). 
with news:
    st.header(f"News of {ticker}")
    sn = StockNews(ticker, save_news=False)
    df_news = sn.read_rss()
    for i in range(5):
        st.subheader(f"News {i+1}")
        st.write(df_news["published"][i])
        st.write(df_news["title"][i])
        st.write(df_news["summary"][i])
        title_sentiment = df_news["sentiment_title"][i]
        st.write(f"Title Sentiment {title_sentiment}")
        news_sentiment = df_news["sentiment_summary"][i]
        st.write(f"News Sentiment {news_sentiment}")
        


   
