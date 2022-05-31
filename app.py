#!/usr/bin/env

import pandas as pd
import streamlit as st
import yfinance as yf
import twint as tw
import datetime as dt


def get_tweets(date, keyword, likes):
    c = tw.Config()
    c.Hide_output = True
    c.Search = keyword
    c.Min_likes = likes
    c.Since = str(date)+" 00:00:00"
    c.Until = str(date)+" 23:59:59"
    c.Pandas = True
    tw.run.Search(c)




st.title("A Tutti piacciono i soldi")
st.header("Twittosity")

with st.form("Paramaters"):
    date = st.date_input("Date")
    keyword = st.text_input("Keyword")
    likes = st.slider("Likes",100,2000,500,10)
    submitted = st.form_submit_button("Search")

if submitted:
    with st.spinner("Wait for it..."):
        get_tweets(date, keyword, likes)
    
    tweets_df = tw.storage.panda.Tweets_df
    
    #cleaned = tweets_df[['tweet','username','nlikes']].sort_values(['nlikes'], ascending=False)

    st.table(tweets_df)




#desired_money = st.slider("Quanti soldi vuoi?", 2, 5002, 2000)


#msft = yf.Ticker("MSFT")

#hist_data = msft.history(period='5y')

start = st.date_input("Enter start date", dt.date(2022, 1, 1))
end = st.date_input("Enter end date", dt.datetime.now().date())

value = yf.download('BTC', start, end)

value['Mean'] = value[['High', 'Low']].mean(axis=1)
st.write(value)
st.line_chart(data=value['Mean'], width=0, height=0, use_container_width=True)
