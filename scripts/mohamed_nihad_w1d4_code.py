import pandas as pd
import streamlit as st
from datetime import date

st.title("💳 Personal Expense Tracker")
st.write("upload a csv with columns:Date,Category,Amount,Description")
st.markdown("---")
uploaded=st.file_uploader("upload a csv",type="csv")
if uploaded is None:
    st.info("Please upload expenses.csv to get started.")
    st.stop()

# Read CSV
df = pd.read_csv(uploaded)

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])




st.subheader("Filters")

# Date Range Picker
date_range = st.date_input(
    "Select Date Range",
    value=(date(2024, 1, 1), date(2024, 5, 31))
)

# Guard before unpacking
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = date(2024, 1, 1)
    end_date = date(2024, 5, 31)

# Apply date filter first
filtered_df = df[
    (df["Date"].dt.date >= start_date) &
    (df["Date"].dt.date <= end_date)
]

# Category Multiselect
all_categories = [
    "Food",
    "Transport",
    "Shopping",
    "Entertainment",
    "Bills",
    "Healthcare"
]

selected_categories = st.multiselect(
    "Select Categories",
    options=all_categories,
    default=all_categories
)

# Guard if user deselects everything
if not selected_categories:
    selected_categories = all_categories

# Apply category filter
filtered_df = filtered_df[
    filtered_df["Category"].isin(selected_categories)
]



st.markdown("                                ")
total_spend = filtered_df["Amount"].sum()
transaction_count = len(filtered_df)
avg_transaction = filtered_df["Amount"].mean()
largest_expense = filtered_df["Amount"].max()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Spend", f"₹{total_spend:,.2f}  ")

with col2:
    st.metric("Transactions", f"{transaction_count}")

with col3:
    st.metric("Average Transaction", f"₹{avg_transaction:,.2f}")

with col4:
    st.metric("Largest Expense", f"₹{largest_expense:,.2f}")




st.subheader("Filtered Transactions")

st.dataframe(
    filtered_df,
    hide_index=True,
    use_container_width=True
)

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name=f"expenses_{start_date}_{end_date}.csv",
    mime="text/csv",
    type="primary"
)


st.subheader("Spend by Category")

bar_color = st.color_picker(
    "Choose Bar Color",
    "#3B82F6"
)

st.write(f"Selected Color: {bar_color}")

category_spend = (
    filtered_df.groupby("Category")["Amount"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(category_spend)



st.subheader("Monthly Summary")

monthly_summary = (
    filtered_df.assign(
        Month=filtered_df["Date"].dt.month_name()
    )
    .groupby("Month")
    .agg(
        Total_Spend=("Amount", "sum"),
        Transaction_Count=("Amount", "count")
    )
)

st.table(monthly_summary)


st.markdown("---")

today = pd.Timestamp.today().strftime("%Y-%m-%d")

st.caption(
    f"Created by Your ubiadu | Personal Expense Tracker | {today}"
)











