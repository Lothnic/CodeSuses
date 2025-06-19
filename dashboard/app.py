import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CodeSnitch Dashboard", layout="wide")

st.title("🚨 CodeSnitch Dashboard")

df = pd.read_csv('enhanced_filtered_users.csv')

total_users = len(df)
cheaters = df[df['cheating'] == True]
cheater_count = len(cheaters)
percent_cheaters = (cheater_count / total_users) * 100

st.metric("Total Users", total_users)
st.metric("Suspicious Users Detected", cheater_count)
st.metric("% Suspicious Users", f"{percent_cheaters:.2f}%")

if 'country' in df.columns:
    st.subheader("🌍 Suspicious Users by Country")
    cheater_country = cheaters['country'].value_counts().reset_index()
    cheater_country.columns = ['country', 'cheater_count']

    fig = px.choropleth(
        cheater_country,
        locations="country",
        locationmode="country names",
        color="cheater_count",
        color_continuous_scale="Blues",
        title="Cheater Density by Country"
    )
    fig.update_layout(
        height=500,  # Fixed height in pixels
        margin=dict(l=0, r=0, t=50, b=0),  # Minimize margins
        dragmode=False  # Disable zoom/pan
    )
    st.plotly_chart(fig, use_container_width=True, config={'scrollZoom': False})

if 'rank' in df.columns:
    st.subheader("📊 Suspicious Users by Rank")
    fig_rank = px.histogram(cheaters, x="rank", title="Suspicious Users Distribution by Rank")
    st.plotly_chart(fig_rank, use_container_width=True)

st.subheader("🔍 Detailed Table View")
only_cheaters = st.checkbox("Show Suspicious Users")
filtered_df = cheaters if only_cheaters else df
st.dataframe(filtered_df.reset_index(drop=True))

csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Filtered CSV", data=csv, file_name='filtered_suspicious_users.csv', mime='text/csv')