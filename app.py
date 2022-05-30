#!/usr/bin/env

import pandas as pd
import streamlit as st
import yfinance as yf
import datetime as dt

st.title("A Tutti piacciono i soldi")

desired_money = st.slider("Quanti soldi vuoi?", 2, 5002, 2000)


#msft = yf.Ticker("MSFT")

#hist_data = msft.history(period='5y')

days = st.slider("Quanti giorni vuoi guardare?", 1, 300, 300)
end = dt.datetime.now()
start = end - dt.timedelta(days=days)

value = yf.download('BTC', start, end)

value['Mean'] = value[['High', 'Low']].mean(axis=1)
st.write(value)
st.line_chart(data=value['Mean'], width=0, height=0, use_container_width=True)