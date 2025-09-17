import streamlit as st
from utils.load_data import load_data
import pandas as pd

df = load_data()

st.title("💰 Profit Analysis")

seg = st.selectbox("Select Segment", ["All"] + list(df["Segment"].unique()))
if seg != "All":
    df = df[df["Segment"] == seg]

profit_by_cat = df.groupby("Category")["Profit"].sum().reset_index()
st.bar_chart(profit_by_cat, x="Category", y="Profit")

st.markdown("### Profit by Sub-Category")
profit_by_sub = df.groupby("Sub-Category")["Profit"].sum().reset_index()
st.bar_chart(profit_by_sub, x="Sub-Category", y="Profit")
