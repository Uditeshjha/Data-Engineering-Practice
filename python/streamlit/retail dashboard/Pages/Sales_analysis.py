import streamlit as st
from utils.load_data import load_data
import pandas as pd
from io import StringIO

# ===== Load =====
df = load_data()

st.title("🛒 Sales Analysis")

# ===== Filters (sidebar) =====
with st.sidebar:
    st.header("Filters")
    region = st.selectbox("Region", ["All"] + sorted(df["Region"].dropna().unique().tolist()))
    segment = st.multiselect("Segment", sorted(df["Segment"].dropna().unique().tolist()))
    category = st.multiselect("Category", sorted(df["Category"].dropna().unique().tolist()))
    ship_mode = st.multiselect("Ship Mode", sorted(df["Ship Mode"].dropna().unique().tolist()))
    # Date range
    min_d, max_d = df["Order Date"].min().date(), df["Order Date"].max().date()
    date_range = st.date_input("Order Date Range", value=(min_d, max_d), min_value=min_d, max_value=max_d)
    top_n = st.slider("Top N (Sub-Categories / Products)", 5, 30, 10)

# Apply filters
fdf = df.copy()
if region != "All":
    fdf = fdf[fdf["Region"] == region]
if segment:
    fdf = fdf[fdf["Segment"].isin(segment)]
if category:
    fdf = fdf[fdf["Category"].isin(category)]
if ship_mode:
    fdf = fdf[fdf["Ship Mode"].isin(ship_mode)]

if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_d, end_d = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    fdf = fdf[(fdf["Order Date"] >= start_d) & (fdf["Order Date"] <= end_d)]

# ===== KPIs =====
total_sales = float(fdf["Sales"].sum())
total_orders = int(fdf["Order ID"].nunique())
total_customers = int(fdf["Customer ID"].nunique())
avg_order_value = (total_sales / total_orders) if total_orders else 0.0
avg_discount = float(fdf["Discount"].mean() * 100) if "Discount" in fdf else 0.0
total_profit = float(fdf["Profit"].sum()) if "Profit" in fdf else 0.0
profit_margin = (total_profit / total_sales * 100) if total_sales else 0.0

# Period-over-period comparison (same length prior period)
delta_days = (fdf["Order Date"].max() - fdf["Order Date"].min()).days + 1 if not fdf.empty else 0
sales_delta_pct = None
if delta_days > 0:
    cur_start = fdf["Order Date"].min().normalize()
    prev_start = cur_start - pd.Timedelta(days=delta_days)
    prev_end = cur_start - pd.Timedelta(days=1)
    pdf = df[(df["Order Date"] >= prev_start) & (df["Order Date"] <= prev_end)]
    prev_sales = float(pdf["Sales"].sum())
    if prev_sales > 0:
        sales_delta_pct = ((total_sales - prev_sales) / prev_sales) * 100

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Sales", f"${total_sales:,.0f}",
          delta=f"{sales_delta_pct:+.1f}%" if sales_delta_pct is not None else None)
c2.metric("Total Orders", f"{total_orders:,}")
c3.metric("Avg Order Value", f"${avg_order_value:,.2f}")
c4.metric("Profit Margin", f"{profit_margin:.2f}%")

c5, c6 = st.columns(2)
c5.metric("Unique Customers", f"{total_customers:,}")
c6.metric("Avg Discount", f"{avg_discount:.2f}%")

st.markdown("---")

# ===== Time Series =====
st.subheader("📈 Sales Trend")
if fdf.empty:
    st.info("No data for the selected filters.")
else:
    # Resample to monthly for stability if span is long; otherwise daily
    span_days = (fdf["Order Date"].max() - fdf["Order Date"].min()).days
    ts = fdf[["Order Date", "Sales"]].set_index("Order Date").sort_index()
    if span_days > 120:
        ts = ts.resample("MS").sum().reset_index()
    else:
        ts = ts.resample("D").sum().reset_index()
    st.line_chart(ts, x="Order Date", y="Sales")

st.markdown("---")

# ===== Category & Sub-Category =====
left, right = st.columns(2)

with left:
    st.subheader("🏷️ Sales by Category")
    sales_by_cat = (
        fdf.groupby("Category", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )
    st.bar_chart(sales_by_cat, x="Category", y="Sales")
    st.dataframe(sales_by_cat.rename(columns={"Sales": "Sales ($)"}))

with right:
    st.subheader("📦 Top Sub-Categories (by Sales)")
    sales_by_sub = (
        fdf.groupby("Sub-Category", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
        .head(top_n)
    )
    st.bar_chart(sales_by_sub, x="Sub-Category", y="Sales")
    st.dataframe(sales_by_sub.rename(columns={"Sales": "Sales ($)"}))

st.markdown("---")

# ===== Geography Breakdown (Region/State/City) =====
st.subheader("🌍 Geography Breakdown")
geo_col = "State" if region != "All" else "Region"
geo_sales = (
    fdf.groupby(geo_col, as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
)
st.bar_chart(geo_sales, x=geo_col, y="Sales")
st.dataframe(geo_sales.rename(columns={"Sales": "Sales ($)"}).head(50))

st.markdown("---")

# ===== Product Rankings =====
st.subheader("🏆 Top Products")
prod_cols = ["Product Name", "Sales", "Quantity", "Profit"] if "Profit" in fdf else ["Product Name", "Sales", "Quantity"]
prod_rank = (
    fdf.groupby("Product Name", as_index=False)
    .agg({"Sales": "sum", "Quantity": "sum", **({"Profit": "sum"} if "Profit" in fdf else {})})
    .sort_values("Sales", ascending=False)
    .head(top_n)
)
st.dataframe(prod_rank)

# ===== Discount vs Sales (scatter) =====
if "Discount" in fdf:
    st.subheader("🪙 Sales vs Discount")
    # Aggregate at order item level to scatter
    sdf = fdf[["Discount", "Sales"]].copy()
    st.scatter_chart(sdf, x="Discount", y="Sales")

# ===== Segment Mix (orders) =====
st.subheader("👥 Orders by Segment")
orders_by_segment = (
    fdf.groupby("Segment", as_index=False)["Order ID"]
    .nunique()
    .sort_values("Order ID", ascending=False)
)
st.bar_chart(orders_by_segment, x="Segment", y="Order ID")
st.dataframe(orders_by_segment.rename(columns={"Order ID": "Orders"}))

# ===== Export current view =====
st.markdown("### ⬇️ Download Current Aggregates")
exports = {
    "sales_by_category.csv": sales_by_cat,
    "sales_by_subcategory_topN.csv": sales_by_sub,
    "geo_sales.csv": geo_sales,
    "top_products.csv": prod_rank,
    "orders_by_segment.csv": orders_by_segment.rename(columns={"Order ID": "Orders"})
}
for name, df_out in exports.items():
    csv_buf = StringIO()
    df_out.to_csv(csv_buf, index=False)
    st.download_button(label=f"Download {name}", data=csv_buf.getvalue(), file_name=name, mime="text/csv")
