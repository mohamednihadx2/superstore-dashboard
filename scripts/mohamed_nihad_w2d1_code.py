import streamlit as st
import pandas as pd

st.title("📊 SuperStore Dashboard")

uploaded_file = st.file_uploader(
    "Upload Superstore CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    @st.cache_data
    def load_data(file):
        return pd.read_csv(
            file,
            parse_dates=["order_date", "ship_date"]
        )

    df = load_data(uploaded_file)

    with st.sidebar:
        st.header("Filters")

        regions = st.multiselect(
            "Region",
            options=df["region"].unique(),
            default=df["region"].unique()
        )

        years = st.multiselect(
            "Year",
            options=sorted(df["order_year"].unique()),
            default=sorted(df["order_year"].unique())
        )

        with st.form("date_filter"):
            start_date = st.date_input(
                "Start Date",
                df["order_date"].min().date()
            )

            end_date = st.date_input(
                "End Date",
                df["order_date"].max().date()
            )

            submitted = st.form_submit_button("Apply")

    filtered_df = df[
        (df["region"].isin(regions)) &
        (df["order_year"].isin(years))
    ]

    if submitted:
        filtered_df = filtered_df[
            filtered_df["order_date"].dt.date.between(
                start_date, end_date
            )
        ]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Sales",
            f"${filtered_df['sales'].sum():,.0f}"
        )

    with col2:
        st.metric(
            "Total Profit",
            f"${filtered_df['profit'].sum():,.0f}"
        )

    with col3:
        st.metric(
            "Average Discount",
            f"{filtered_df['discount'].mean()*100:.1f}%"
        )

    tab1, tab2, tab3 = st.tabs(
        ["📊 Overview", "📦 By Category", "🌍 By Region"]
    )

    with tab1:
        st.subheader("Overview")
        st.dataframe(
            filtered_df.head(20),
            use_container_width=True
        )

    with tab2:
        st.info("Category charts arrive on Day 7.")

    with tab3:
        st.info("Region charts arrive on Day 7.")

    st.markdown("---")

    st.caption(
        f"Showing {len(filtered_df):,} rows • "
        f"{filtered_df['order_date'].min().year}-"
        f"{filtered_df['order_date'].max().year} • "
        f"Built by mohamed_nihad_bin"
    )

else:
    st.info("Please upload superstore_clean.csv to continue.")