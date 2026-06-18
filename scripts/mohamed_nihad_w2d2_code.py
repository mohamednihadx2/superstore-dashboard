import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import pandas as pd

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

# Top 10 sub-categories by sales
top10_subcat = (
    df.groupby("sub_category")["sales"]
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

ax.set_title("Top 10 Sub-Categories by Sales")
ax.set_xlabel("Sales ($)")
ax.set_ylabel("Sub-Category")

st.pyplot(fig)
plt.close(fig)

fig = px.scatter(
    df,
    x="sales",
    y="profit",
    color="category",          # Color by product category
    size="quantity",           # Bubble size by quantity ordered
    hover_data=["sub_category"],
    title="Sales vs Profit by Category"
)
st.plotly_chart(fig, use_container_width=True)

df["order_year"] = df["order_date"].dt.year
df["month_period"] = df["order_date"].dt.strftime("%b")

monthly_sales = (
    df.groupby(["order_year", "month_period"], as_index=False)["sales"]
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