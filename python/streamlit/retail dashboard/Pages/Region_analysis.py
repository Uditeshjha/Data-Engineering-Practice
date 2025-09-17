import streamlit as st
from utils.load_data import load_data
import pandas as pd

# Load data
df = load_data()

st.title("🌍 Region Analysis Dashboard")

# =========================
# Filters
# =========================
st.sidebar.header("🔎 Filters")
region_filter = st.sidebar.multiselect("Select Region(s)", options=df["Region"].unique(), default=df["Region"].unique())
date_range = st.sidebar.date_input("Select Date Range", [df["Order Date"].min(), df["Order Date"].max()])

# Apply filters
df = df[df["Region"].isin(region_filter)]
df = df[(df["Order Date"] >= pd.to_datetime(date_range[0])) & (df["Order Date"] <= pd.to_datetime(date_range[1]))]

# =========================
# KPIs
# =========================
st.subheader("📌 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${df['Sales'].sum():,.0f}")
col2.metric("Total Profit", f"${df['Profit'].sum():,.0f}")
col3.metric("Total Orders", df["Order ID"].nunique())
col4.metric("Total Customers", df["Customer ID"].nunique())

st.markdown("---")

# =========================
# Sales by Region
# =========================
st.subheader("💰 Sales by Region")
sales_region = df.groupby("Region")["Sales"].sum().reset_index()
st.bar_chart(sales_region, x="Region", y="Sales")

# =========================
# Profit by Region
# =========================
st.subheader("📈 Profit by Region")
profit_region = df.groupby("Region")["Profit"].sum().reset_index()
st.bar_chart(profit_region, x="Region", y="Profit")

# =========================
# Sales vs Profit Trend by Region
# =========================
st.subheader("📊 Sales & Profit Trend by Region")
trend = df.groupby(["Order Date", "Region"])[["Sales", "Profit"]].sum().reset_index()
st.line_chart(trend, x="Order Date", y=["Sales", "Profit"], color="Region")

# =========================
# Sales Share by Region (Pie Chart)
# =========================
st.subheader("🥧 Sales Share by Region")
sales_share = df.groupby("Region")["Sales"].sum()
st.pyplot(sales_share.plot.pie(autopct="%1.1f%%", figsize=(6,6), ylabel="").get_figure())

# =========================
# Top 5 States in Selected Regions
# =========================
st.subheader("🏆 Top 5 States by Sales")
top_states = df.groupby("State")["Sales"].sum().reset_index().sort_values(by="Sales", ascending=False).head(5)
st.table(top_states)

# =========================
# Customer Segment Contribution by Region
# =========================
st.subheader("👥 Segment Contribution by Region")
seg_region = df.groupby(["Region", "Segment"])["Sales"].sum().reset_index()
st.bar_chart(seg_region, x="Region", y="Sales", color="Segment")
