import pandas as pd
import streamlit as st

data={
    "Name":["Aisha","Bob","Clara","Dev","Eva","Finn","Grace","Hiro","Ines","Jay"],
    "Math":   [88,52,76,91,43,67,85,59,78,95],
    "Science":[72,45,88,83,38,71,90,62,55,80],
    "English":[65,70,82,77,60,58,74,88,91,73],
    "Art":    [90,85,60,55,78,92,68,75,83,61]
}
df=pd.DataFrame(data)
df["Average"]=df[["Math","Science","English","Art"]].mean(axis=1).round(1)
st.title("📊Student perfomence Dashboard")
st.write(f"Total Students: {len(df)}")


class_avg = round(df["Average"].mean(), 1)
highest_avg = round(df["Average"].max(), 1)
lowest_avg = round(df["Average"].min(), 1)
above_70 = (df["Average"] >= 70).sum()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Class Average", class_avg)
c2.metric("Highest Average", highest_avg)
c3.metric("Lowest Average", lowest_avg)
c4.metric("Average ≥ 70", above_70)

styled_df = df.style.map(
    lambda v: "color:green" if v >= 70 else "color:red",
    subset=["Average"]
)

st.subheader("Student Marks")

st.dataframe(
    styled_df,
    hide_index=True,
    use_container_width=True
)
top3 = (
    df.sort_values("Average", ascending=False)
      .head(3)
      .reset_index(drop=True)
)

top3.index = top3.index + 1
st.subheader("🏆 Top 3 Students")

st.table(top3)
subjects = ["Math", "Science", "English", "Art"]

summary = {}

for subject in subjects:
    summary[subject] = {
        "Minimum": int(df[subject].min()),
        "Maximum": int(df[subject].max()),
        "Mean": round(df[subject].mean(), 1)
    }
st.subheader("📚 Subject Summary")

st.json(summary)

st.markdown("---")

st.caption(
    f"Created by mohamed nihad | Student Grade Dashboard | 04-jun-2026"
)




