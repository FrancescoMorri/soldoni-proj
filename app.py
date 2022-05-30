from pandas import Period
import streamlit as st
import yfinance as yf

st.title("A Tutti piacciono i soldi")
st.subtitle("Test branch")

desired_money = st.slider("Quanti soldi vuoi?", 2, 5002, 2000)

msft = yf.Ticker("MSFT")

hist_data = msft.history(period='5y')

st.write(hist_data)