#!/usr/bin/env

import pandas as pd
import streamlit as st
import yfinance as yf
import twint as tw
import datetime as dt
import matplotlib.pyplot as plt
import altair as alt


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
        
    source = pd.DataFrame(tmp, columns=['date','n_tweet'])

    value = yf.download('BTC-EUR', start, end)

    source['Mean'] = list(value[['High', 'Low']].mean(axis=1))
    
    

    base = alt.Chart(source).encode(
        x=alt.X('date', axis=alt.Axis(title="Date"))
    )

    twit = base.mark_line(stroke='blue').encode(
        y=alt.Y('n_tweet', axis=alt.Axis(title="Number of tweets per day"))
    )

    money = base.mark_line(stroke='green').encode(
        y=alt.Y('Mean', axis=alt.Axis(title="BTC-EUR"))
    )

    g = alt.layer(twit, money).resolve_scale(
        y='independent'
    ).interactive()

    st.altair_chart(g, use_container_width=True)

