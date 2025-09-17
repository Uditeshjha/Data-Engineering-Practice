import streamlit as st
from utils.load_data import load_data

df = load_data()

st.title("📦 Category Analysis")

cat = st.selectbox("Select Category", df["Category"].unique())
df_cat = df[df["Category"] == cat]

st.subheader(f"Sales by Sub-Category in {cat}")
sales_sub = df_cat.groupby("Sub-Category")["Sales"].sum().reset_index()
st.bar_chart(sales_sub, x="Sub-Category", y="Sales")

st.subheader(f"Profit by Sub-Category in {cat}")
profit_sub = df_cat.groupby("Sub-Category")["Profit"].sum().reset_index()
st.bar_chart(profit_sub, x="Sub-Category", y="Profit")
