import streamlit as st
from utils.load_data import load_data

st.set_page_config(page_title="Superstore Dashboard", page_icon="🛍️", layout="wide")

st.title("🛍️ Superstore Sales Analysis Dashboard")

st.markdown("""
Welcome to the *Superstore Analytics Dashboard* built with *Streamlit*.  
Use the sidebar to navigate between different analysis modules:
* 📊 Overview  
* 🛒 Sales Analysis  
* 💰 Profit Analysis  
* 🌍 Region Analysis  
* 📦 Category Analysis
""")

st.markdown("---")
st.subheader("Upload / Use Default Dataset")

uploaded_file = st.file_uploader("Upload your Superstore CSV file", type=["excel", "csv","xls"])
if uploaded_file:
    df = load_data(uploaded_file)
else:
    df = load_data()

st.dataframe(df.head(10))