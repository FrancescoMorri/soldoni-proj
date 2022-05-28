from pandas import Period
import streamlit as st
import yfinance as yf

st.title("A Squadra piacciono i soldi")

msft = yf.Ticker("MSFT")

hist_data = msft.history(period='5y')

st.write(hist_data)