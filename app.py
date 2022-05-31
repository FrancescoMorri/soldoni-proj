#!/usr/bin/env

import pandas as pd
import streamlit as st
import yfinance as yf
import twint as tw
import datetime as dt
import matplotlib.pyplot as plt


def get_tweets(date, keyword, likes):
    c = tw.Config()
    c.Hide_output = True
    c.Search = keyword
    c.Min_likes = likes
    c.Since = str(date)
    c.Until = str(date+dt.timedelta(hours=23, minutes=59, seconds=59))
    c.Pandas = True
    tw.run.Search(c)




st.title("A Tutti piacciono i soldi")
st.header("Twittosity")



with st.form("Paramaters"):
    start = st.date_input("Enter start date", dt.date(2022, 1, 1))
    end = st.date_input("Enter end date", dt.datetime.now().date())
    keyword = "bitcoin"
    likes = st.slider("Likes",100,2000,500,10)
    submitted = st.form_submit_button("Search")

if submitted:
    tmp = []
    dates_window = pd.date_range(start=start, end=end)
    bar = st.progress(0)
    tot_len = len(dates_window)
    for i, day in enumerate(dates_window):
        get_tweets(day, keyword, likes)
        bar.progress((i+1)/tot_len)
        tweets_df = tw.storage.panda.Tweets_df
        if tweets_df.empty:
            tmp.append([day.date(),0])
        else:
            tmp.append([day.date(),len(tweets_df['tweet'])])
        
    twittosity = pd.DataFrame(tmp, columns=['date','n_tweet'])

    value = yf.download('BTC-EUR', start, end)

    value['Mean'] = value[['High', 'Low']].mean(axis=1)
    
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    fig, ax1 = plt.subplots()
    ax1.plot(value['Mean'], color='red')
    ax1.xaxis.set_major_locator(plt.MaxNLocator(5))
    ax2 = ax1.twinx()
    ax2.plot(twittosity['date'], twittosity['n_tweet'], color='blue')
    ax2.xaxis.set_major_locator(plt.MaxNLocator(5))
    fig.tight_layout()
    

    st.pyplot(fig)
