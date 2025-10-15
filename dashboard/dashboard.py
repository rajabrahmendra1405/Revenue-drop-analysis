import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# =========================
# Setup
# =========================
st.set_page_config(page_title="Revenue Drop Analysis", layout="wide")
os.makedirs("reports", exist_ok=True)

# Load dataset
df = pd.read_excel("data/ecommerce_sales.xlsx")

# Convert Date and add Month column
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.to_period("M")
df["Revenue"] = df["Total Sales"]

# =========================
# Sidebar Filters
# =========================
st.sidebar.header("Filters")

selected_category = st.sidebar.selectbox(
    "Select Product Category", 
    ["All"] + list(df["Product Category"].unique()), 
    key="category_select"
)

selected_payment = st.sidebar.selectbox(
    "Select Payment Method", 
    ["All"] + list(df["Payment Method"].unique()), 
    key="payment_select"
)

selected_month = st.sidebar.selectbox(
    "Select Month", 
    ["All"] + list(df["Month"].astype(str).unique()), 
    key="month_select"
)

# =========================
# Apply Filters
# =========================
filtered_df = df.copy()
if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Product Category"] == selected_category]
if selected_payment != "All":
    filtered_df = filtered_df[filtered_df["Payment Method"] == selected_payment]
if selected_month != "All":
    filtered_df = filtered_df[filtered_df["Month"].astype(str) == selected_month]

# =========================
# Revenue Overview
# =========================
st.title("📊 E-Commerce Revenue Drop Analysis")

total_revenue = filtered_df["Revenue"].sum()
st.metric("Total Revenue", f"${total_revenue:,.2f}")

st.subheader("Revenue Trend Over Time")
monthly_revenue = filtered_df.groupby("Month")["Revenue"].sum()
fig, ax = plt.subplots(figsize=(10,4))
monthly_revenue.plot(marker='o', color="green", ax=ax)
ax.set_ylabel("Revenue")
ax.set_xlabel("Month")
ax.set_title("Monthly Revenue Trend")
st.pyplot(fig)

# =========================
# Revenue Drop Detection
# =========================
revenue_change = monthly_revenue.pct_change().fillna(0)
drop_month = revenue_change.idxmin()
drop_value = revenue_change.min()

st.subheader("Revenue Drop Analysis")
st.write(f"📉 Largest revenue drop of **{drop_value:.2%}** occurred in **{drop_month}**")

fig, ax = plt.subplots(figsize=(10,4))
revenue_change.plot(marker='o', color="red", ax=ax)
ax.set_ylabel("Revenue % Change")
ax.set_xlabel("Month")
ax.set_title("Month-over-Month Revenue Change")
st.pyplot(fig)

# =========================
# Top Products Analysis
# =========================
st.subheader("Top 5 Best-Selling Products")
top_products = filtered_df.groupby("Product Name")["Quantity Sold"].sum().sort_values(ascending=False).head(5)
fig, ax = plt.subplots(figsize=(10,4))
top_products.plot(kind="bar", color="skyblue", ax=ax)
ax.set_ylabel("Quantity Sold")
ax.set_xlabel("Product Name")
ax.set_title("Top 5 Products")
st.pyplot(fig)

# Revenue by Category
st.subheader("Revenue Breakdown by Product Category")
category_revenue = filtered_df.groupby("Product Category")["Revenue"].sum()
fig, ax = plt.subplots()
category_revenue.plot(kind="pie", autopct="%1.1f%%", ax=ax)
ax.set_ylabel("")
st.pyplot(fig)

# =========================
# Discount Impact Analysis
# =========================
st.subheader("Discount Impact Analysis")
if "Discount Applied" in df.columns:
    discount_trend = filtered_df.groupby("Month")["Discount Applied"].mean()
    fig, ax = plt.subplots(figsize=(10,4))
    discount_trend.plot(marker='o', color="purple", ax=ax)
    ax.set_ylabel("Average Discount (%)")
    ax.set_xlabel("Month")
    ax.set_title("Average Discount Over Time")
    st.pyplot(fig)
    corr = filtered_df["Revenue"].corr(filtered_df["Discount Applied"])
    st.write(f"Correlation between discount and revenue: {corr:.2f}")

# =========================
# Sales Drop Reasons
# =========================
st.subheader("Sales Drop Reasons Analysis")
before_drop = filtered_df[filtered_df["Month"] < drop_month].groupby("Product Name")["Revenue"].sum()
during_drop = filtered_df[filtered_df["Month"] == drop_month].groupby("Product Name")["Revenue"].sum()
drop_comp = pd.concat([before_drop, during_drop], axis=1, keys=["Before", "During"]).fillna(0)
drop_comp["Change_%"] = ((drop_comp["During"] - drop_comp["Before"]) / drop_comp["Before"]) * 100
drop_comp_sorted = drop_comp.sort_values("Change_%")

st.write("**Top 5 products contributing to drop:**")
st.dataframe(drop_comp_sorted.head(5))
drop_comp_sorted.to_csv("reports/revenue_drop_top_products.csv", index=True)

# Waterfall chart
st.subheader("Waterfall Chart: Contribution of Top Products to Revenue Drop")
top_contributors = drop_comp_sorted.head(10)
fig, ax = plt.subplots(figsize=(12,5))
ax.bar(top_contributors.index, top_contributors["Change_%"], color="tomato")
ax.set_ylabel("Revenue % Change")
ax.set_title("Top Product Contribution to Revenue Drop")
plt.xticks(rotation=45, ha="right")
st.pyplot(fig)

# =========================
# Affected Segments
# =========================
st.subheader("Top Affected Segments")
segments = ["Product Category", "Payment Method"]
for seg in segments:
    before = filtered_df[filtered_df["Month"] < drop_month].groupby(seg)["Revenue"].sum()
    during = filtered_df[filtered_df["Month"] == drop_month].groupby(seg)["Revenue"].sum()
    comp = pd.concat([before, during], axis=1, keys=["Before", "During"]).fillna(0)
    comp["Change_%"] = ((comp["During"] - comp["Before"]) / comp["Before"]) * 100
    comp = comp.sort_values("Change_%")
    
    st.write(f"**Top 5 affected {seg}s:**")
    st.dataframe(comp.head(5))
    comp.to_csv(f"reports/top_affected_{seg.replace(' ','_')}.csv")

# =========================
# Revenue Heatmap
# =========================
st.subheader("Revenue Heatmap by Category & Payment Method")
pivot = filtered_df.pivot_table(index="Product Category", columns="Payment Method", values="Revenue", aggfunc='sum').fillna(0)
fig, ax = plt.subplots(figsize=(10,6))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="Reds", ax=ax)
ax.set_title("Revenue Heatmap")
st.pyplot(fig)

# =========================
# Save Filtered Data
# =========================
filtered_df.to_csv("reports/filtered_sales.csv", index=False)
st.success("Filtered data saved to reports/filtered_sales.csv")

# =========================
# Automated Insights
# =========================
st.subheader("Automated Insights")
insights = []
if drop_value < 0:
    insights.append(f"Revenue dropped {abs(drop_value*100):.2f}% in {drop_month}.")
if "Discount Applied" in df.columns and corr < 0:
    insights.append("Increase in discount may have negatively impacted revenue.")
top_drop_products = drop_comp_sorted.head(3).index.tolist()
insights.append(f"Top products contributing to drop: {', '.join(top_drop_products)}.")
st.write("💡 " + " ".join(insights))
