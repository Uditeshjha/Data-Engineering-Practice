import streamlit as st
from utils.load_data import load_data
import pandas as pd

df = load_data()

st.title("📊 Overview Dashboard")

# ===================== KPIs =====================
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
total_orders = df['Order ID'].nunique()
total_customers = df['Customer ID'].nunique()
avg_order_value = total_sales / total_orders
profit_margin = (total_profit / total_sales) * 100

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Total Orders", total_orders)

col4, col5, col6 = st.columns(3)
col4.metric("Unique Customers", total_customers)
col5.metric("Avg Order Value", f"${avg_order_value:,.2f}")
col6.metric("Profit Margin", f"{profit_margin:.2f}%")

st.markdown("---")

# ===================== Sales Trend =====================
st.subheader("📈 Sales Trend Over Time")
sales_trend = df.groupby('Order Date')['Sales'].sum().reset_index()
st.line_chart(sales_trend, x="Order Date", y="Sales")

# ===================== Profit Trend =====================
st.subheader("💹 Profit Trend Over Time")
profit_trend = df.groupby('Order Date')['Profit'].sum().reset_index()
st.line_chart(profit_trend, x="Order Date", y="Profit")

st.markdown("---")

# ===================== Breakdown Analysis =====================
st.subheader("🛒 Sales by Category")
sales_by_category = df.groupby("Category")["Sales"].sum().reset_index()
st.bar_chart(sales_by_category, x="Category", y="Sales")

st.subheader("💰 Profit by Region")
profit_by_region = df.groupby("Region")["Profit"].sum().reset_index()
st.bar_chart(profit_by_region, x="Region", y="Profit")

st.subheader("👥 Orders by Segment")
orders_by_segment = df.groupby("Segment")["Order ID"].nunique().reset_index()
st.bar_chart(orders_by_segment, x="Segment", y="Order ID")
