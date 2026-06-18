import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
st.set_page_config(
    page_title="Superstore Dashboard",
    page_icon="📊",
    layout="wide"
)

# --------------------------------
# Load Data
# --------------------------------
@st.cache_data
def load_data():
    return pd.read_csv(
        r"C:\Users\moham\OneDrive\Desktop\project_4.1\Output\superstore_cleaned.csv",
        parse_dates=["order_date", "ship_date"]
    )

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading file: {e}")
    st.stop()

# --------------------------------
# Page Title
# --------------------------------
st.title("📊 Superstore Dashboard")
st.markdown("Interactive dashboard for Superstore sales analysis")

df["order_year"] = df["order_date"].dt.year

df["month_period"] = df["order_date"].dt.strftime("%b")

# =========================
# SIDEBAR FILTERS
# =========================

with st.sidebar:

    st.header("Filters")

    selected_regions = st.multiselect(
        "Region",
        options=sorted(df["region"].unique()),
        default=sorted(df["region"].unique())
    )

    selected_years = st.multiselect(
        "Year",
        options=sorted(df["order_year"].unique()),
        default=sorted(df["order_year"].unique())
    )

    start_date = st.date_input(
        "Start Date",
        value=df["order_date"].min().date()
    )

    end_date = st.date_input(
        "End Date",
        value=df["order_date"].max().date()
    )

filtered = df[
    (df["region"].isin(selected_regions)) &
    (df["order_year"].isin(selected_years))
]

filtered = filtered[
    filtered["order_date"].dt.date.between(
        start_date,
        end_date
    )
]

filtered["month_period"] = filtered["order_date"].dt.strftime("%b")
 # percentiles
     # ensure numeric numpy array (coerce non-numeric to NaN, drop them)
arr = pd.to_numeric(df["discount"], errors="coerce").dropna().to_numpy(dtype=float)

if arr.size > 0:
        per75 = np.percentile(arr, 75)
else:
        per75 = 0.0
high = df[pd.to_numeric(df["discount"], errors="coerce") > per75]

print(f"75th percentile of discount: {per75:.2f}")
print(f"Number of high discount records: {len(high)}")


    # ensure numeric numpy array for sales, handle empty or constant arrays
sales_arr = pd.to_numeric(filtered["sales"], errors="coerce").dropna().to_numpy(dtype=float)
if sales_arr.size == 0:
        z = np.array([])
else:
        std = np.std(sales_arr)
        if std == 0:
            z = np.zeros_like(sales_arr)
        else:
            z = (sales_arr - np.mean(sales_arr)) / std
outliers = filtered.iloc[np.where(np.abs(z) > 2)[0]] if z.size > 0 else filtered.iloc[0:0]
print(f"outliers detected: {len(outliers)}")

# =========================
# KPI ROW
# =========================

st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Sales",
        f"${filtered['sales'].sum():,.0f}"
    )

with col2:
    st.metric(
        "Total Profit",
        f"${filtered['profit'].sum():,.0f}"
    )

with col3:
    st.metric(
        "Average Discount",
        f"{filtered['discount'].mean():.1%}"
    )

# =========================
# CHARTS
# =========================

col1, col2 = st.columns(2)

with col1:

    st.subheader("Sales by Category")

    category_sales = (
        filtered.groupby("category")["sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_sales)

with col2:

    st.subheader("Profit by Category")

    category_profit = (
        filtered.groupby("category")["profit"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_profit)

# =========================
# SALES TREND
# =========================

st.subheader("Monthly Sales Trend")

monthly_sales = (
    filtered.groupby(
        filtered["order_date"].dt.to_period("M")
    )["sales"]
    .sum()
)

monthly_sales.index = monthly_sales.index.astype(str)

st.line_chart(monthly_sales)

# =========================
# DATA TABLE
# =========================

st.subheader("Filtered Data")

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)

# =========================
# DOWNLOAD BUTTON
# =========================

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Filtered Data",
    data=csv,
    file_name="filtered_superstore.csv",
    mime="text/csv"
)

# =========================
# TASK 5 - TABS
# =========================

tab1, tab2, tab3,tab4 = st.tabs(
    ["📋 Overview", "📦 By Category", "🗺️ By Region"," 🚨Quality Alerts"]
)

# Overview Tab
with tab1:
    st.subheader("Filtered Data Preview")

    monthly_sales = (
    filtered.groupby(["order_year", "month_period"], as_index=False)["sales"]
      .sum()
    )

    fig = px.line(
    monthly_sales,
    x="month_period",
    y="sales",
    color="order_year",
    title="Monthly Sales Trend by Category"
    )
    st.plotly_chart(fig, use_container_width=True)


# By Category Tab
with tab2:
    st.subheader("Sales by Category")

    # Top 10 sub-categories by sales
    top10_subcat = (
    filtered.groupby("sub_category")["sales"]
      .sum()
      .nlargest(10)          # Get top 10
      .sort_values()         # Sort ascending for horizontal bar chart
    )

    fig, ax = plt.subplots(figsize=(7, 4))

    bars = ax.barh(
    top10_subcat.index,
    top10_subcat.values, # pyright: ignore[reportArgumentType]
    color="#3B82F6"

    )

    # Add dollar value labels
    ax.bar_label(
    bars,
    fmt="${:,.0f}",
    padding=4,
    fontsize=8
    )

    # Set axis labels and title
    ax.set_title("Top 10 Sub-Categories by Sales")
    ax.set_xlabel("Sales ($)")
    ax.set_ylabel("Sub-Category")

    st.pyplot(fig)
    plt.close(fig)

    fig = px.scatter(
    filtered,
    x="sales",
    y="profit",
    color="category",          # Color by product category
    size="quantity",           # Bubble size by quantity ordered
    hover_data=["sub_category"],
    title="Sales vs Profit by Category"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Sub-Category Breakdown")

    subcategory_summary = (
        filtered.groupby("sub_category")
        .agg(
            Total_Sales=("sales", "sum"),
            Total_Profit=("profit", "sum")
        )
        .sort_values(
            by="Total_Sales",
            ascending=False
        )
    )

    st.dataframe(
        subcategory_summary.style.format("${:,.0f}"),
        use_container_width=True
    )


# By Region Tab
with tab3:

    st.subheader("Sales by Region")

    # Total profit by region
    region_profit = (
        filtered.groupby("region")["profit"]
          .sum()
          .reset_index()
    )

    # Donut chart
    fig = px.pie(
        region_profit,
        names="region",
        values="profit",
        hole=0.4,
        title="Region Share of Total Profit"
    )

    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("Quality Alerts")

    mean_margin = (filtered["profit"].sum() / filtered["sales"].sum()) * 100

    if mean_margin < 10:
         st.error(f"critical {mean_margin:.2f}% - urgent action needed!")
    elif mean_margin < 20:
        st.warning(f"moderate {mean_margin:.2f}% - improvement needed!")
    else:
        st.success(f"healthy {mean_margin:.2f}% - good performance!")


    st.info(f"75th percentile of discount: {per75:.2f}")
    if len(high) > 0:
        st.warning(f"Number of high discount records: {len(high)}")
    else:
        st.success("No high discount records found.")

    with st.expander("show raw data(first 50 rows)"):
        st.dataframe(filtered.head(50), use_container_width=True)


# =========================
# TASK 6 - FOOTER CAPTION
# =========================

st.markdown("---")

row_count = len(filtered)

min_year = filtered["order_year"].min()
max_year = filtered["order_year"].max()

st.caption(
    f"Showing {row_count:,} rows • "
    f"{min_year}–{max_year} • "
    f"Built by Mohammed minshan"
)