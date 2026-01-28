# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 21:32:19 2026

@author: VMfidi
"""

import streamlit as st
import pandas as pd
import sqlite3
import altair as alt

# Page config
st.set_page_config(
    page_title="Top Play Store Food Apps",
    layout="wide"
)


# Title & description
st.title("Top Food Apps on Google Play Store")
st.caption("Analysis based on ratings, reviews, and sentiment polarity")

# Load data from SQLite
@st.cache_data
def load_data():
    conn = sqlite3.connect("market_research")  # Update if your DB has an extension
    df = pd.read_sql(
        """
        SELECT
            *
        FROM top_apps
        """,
        conn
    )
    conn.close()
    return df

df = load_data()


# Show full dataset first
st.subheader("All App Data")
st.dataframe(
    df[["App", "Rating", "Reviews", "Sentiment_Polarity"]].sort_values("Rating", ascending=False),
    use_container_width =True
)

# KPI metrics
col1, col2, col3 = st.columns(3)

col1.metric(" Average Rating", round(df["Rating"].mean(), 2))
col2.metric("Total Apps", len(df))
col3.metric(
    " Avg Sentiment",
    round(df["Sentiment_Polarity"].mean(), 2)
    if df["Sentiment_Polarity"].notna().any()
    else "N/A"
)

st.divider()


# Sidebar filters
st.sidebar.header("Filters")

min_rating = st.sidebar.slider(
    "Minimum Rating",
    min_value=float(df["Rating"].min()),
    max_value=5.0,
    value=4.5,
    step=0.1
)

top_n = st.sidebar.slider(
    "Show Top N Apps",
    min_value=3,
    max_value=len(df),
    value=5
)

# Filter dataframe based on slider
filtered_df = df[df["Rating"] >= min_rating]

# # Top apps by rating
st.subheader("App Quality vs Popularity")

bubble_chart = alt.Chart(filtered_df).mark_circle(opacity=0.7).encode(
    x=alt.X(
        "Reviews:Q",
        scale=alt.Scale(type="log"),
        title="Number of Reviews (log scale)"
    ),
    y=alt.Y(
        "Rating:Q",
        scale=alt.Scale(domain=[4.4, 5.0]),
        title="Rating"
    ),
    size=alt.Size(
        "Sentiment_Polarity:Q",
        title="Sentiment Polarity",
        scale=alt.Scale(range=[100, 2000])
    ),
    color=alt.Color("App:N", legend=None),
    tooltip=["App", "Rating", "Reviews", "Sentiment_Polarity"]
).interactive()

st.altair_chart(bubble_chart, use_container_width=True)
# Sentiment analysis
sentiment_df = filtered_df.dropna(subset=["Sentiment_Polarity"])
if not sentiment_df.empty:
    st.subheader("User Sentiment Polarity")
    sentiment_chart = alt.Chart(sentiment_df).mark_bar().encode(
        x=alt.X("Sentiment_Polarity", title="Sentiment Polarity"),
        y=alt.Y("App", sort="-x"),
        tooltip=["App", "Sentiment_Polarity"]
    )
    st.altair_chart(sentiment_chart, use_container_width=True)







