import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Financial Transactions Dashboard",
    page_icon="💰",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("Financial Transactions Data Analysis")
st.markdown(
    "Interactive dashboard for analyzing synthetic financial transactions "
    "using NumPy, Pandas, Streamlit and Plotly."
)


# =========================================================
# GENERATE SYNTHETIC DATA
# =========================================================

np.random.seed(42)

n = 2000000

df = pd.DataFrame({
    "Transaction_ID": np.arange(1, n + 1),

    "Customer_ID": np.random.randint(
        1000,
        10000,
        n
    ),

    "Customer_Age": np.random.randint(
        18,
        70,
        n
    ),

    "Transaction_Date": pd.to_datetime(
        np.random.choice(
            pd.date_range(
                "2024-01-01",
                "2026-08-31"
            ),
            n
        )
    ),

    "Transaction_Amount": np.round(
        np.random.uniform(
            10,
            10000,
            n
        ),
        2
    ),

    "Payment_Method": np.random.choice(
        [
            "Card",
            "Mobile Money",
            "Bank Transfer",
            "Cash",
            "Online"
        ],
        n
    ),

    "Transaction_Channel": np.random.choice(
        [
            "ATM",
            "POS",
            "Online",
            "Mobile App",
            "Bank Branch"
        ],
        n
    ),

    "Currency": np.random.choice(
        [
            "KES",
            "USD",
            "EUR",
            "GBP"
        ],
        n
    ),

    "Fraud_Flag": np.random.choice(
        [
            0,
            1
        ],
        n,
        p=[
            0.97,
            0.03
        ]
    ),

    "Risk_Score": np.random.randint(
        1,
        101,
        n
    )
})


# =========================================================
# CREATE ADDITIONAL COLUMNS USING PANDAS
# =========================================================

df["Year"] = df["Transaction_Date"].dt.year

df["Month"] = df["Transaction_Date"].dt.month

df["Month_Name"] = df["Transaction_Date"].dt.strftime("%B")

df["Day"] = df["Transaction_Date"].dt.day

df["Day_Name"] = df["Transaction_Date"].dt.strftime("%A")

df["Quarter"] = df["Transaction_Date"].dt.quarter

df["Fraud_Status"] = df["Fraud_Flag"].map({
    0: "Legitimate",
    1: "Fraud"
})

df["Risk_Level"] = pd.cut(
    df["Risk_Score"],
    bins=[
        0,
        30,
        70,
        100
    ],
    labels=[
        "Low Risk",
        "Medium Risk",
        "High Risk"
    ]
)


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("Dashboard Filters")

selected_currency = st.sidebar.multiselect(
    "Select Currency",
    options=sorted(df["Currency"].unique()),
    default=sorted(df["Currency"].unique())
)

selected_payment = st.sidebar.multiselect(
    "Select Payment Method",
    options=sorted(df["Payment_Method"].unique()),
    default=sorted(df["Payment_Method"].unique())
)

selected_channel = st.sidebar.multiselect(
    "Select Transaction Channel",
    options=sorted(df["Transaction_Channel"].unique()),
    default=sorted(df["Transaction_Channel"].unique())
)

selected_fraud = st.sidebar.multiselect(
    "Fraud Status",
    options=sorted(df["Fraud_Status"].unique()),
    default=sorted(df["Fraud_Status"].unique())
)

min_age, max_age = st.sidebar.slider(
    "Customer Age",
    min_value=int(df["Customer_Age"].min()),
    max_value=int(df["Customer_Age"].max()),
    value=(
        int(df["Customer_Age"].min()),
        int(df["Customer_Age"].max())
    )
)


# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df[
    (df["Currency"].isin(selected_currency))
    &
    (df["Payment_Method"].isin(selected_payment))
    &
    (df["Transaction_Channel"].isin(selected_channel))
    &
    (df["Fraud_Status"].isin(selected_fraud))
    &
    (df["Customer_Age"].between(min_age, max_age))
].copy()


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_transactions = len(filtered_df)

total_amount = filtered_df["Transaction_Amount"].sum()

average_transaction = filtered_df["Transaction_Amount"].mean()

unique_customers = filtered_df["Customer_ID"].nunique()

fraud_transactions = (
    filtered_df["Fraud_Flag"].sum()
)

fraud_rate = (
    fraud_transactions / total_transactions * 100
    if total_transactions > 0
    else 0
)

average_risk = filtered_df["Risk_Score"].mean()


# =========================================================
# KPI CARDS
# =========================================================

st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Transactions",
        f"{total_transactions:,}"
    )

with col2:
    st.metric(
        "Total Transaction Amount",
        f"{total_amount:,.2f}"
    )

with col3:
    st.metric(
        "Average Transaction",
        f"{average_transaction:,.2f}"
    )

with col4:
    st.metric(
        "Unique Customers",
        f"{unique_customers:,}"
    )


col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        "Fraud Transactions",
        f"{fraud_transactions:,}"
    )

with col6:
    st.metric(
        "Fraud Rate",
        f"{fraud_rate:.2f}%"
    )

with col7:
    st.metric(
        "Average Risk Score",
        f"{average_risk:.2f}"
    )

with col8:
    st.metric(
        "Maximum Transaction",
        f"{filtered_df['Transaction_Amount'].max():,.2f}"
    )


# =========================================================
# TRANSACTION TRENDS
# =========================================================

st.subheader("Transaction Trends")

monthly_transactions = (
    filtered_df
    .groupby(
        filtered_df["Transaction_Date"].dt.to_period("M")
    )
    .agg(
        Transactions=("Transaction_ID", "count"),
        Total_Amount=("Transaction_Amount", "sum")
    )
    .reset_index()
)

monthly_transactions["Transaction_Date"] = (
    monthly_transactions["Transaction_Date"]
    .astype(str)
)


col1, col2 = st.columns(2)

with col1:

    fig = px.line(
        monthly_transactions,
        x="Transaction_Date",
        y="Transactions",
        markers=True,
        title="Number of Transactions Over Time"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Number of Transactions",
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    fig = px.line(
        monthly_transactions,
        x="Transaction_Date",
        y="Total_Amount",
        markers=True,
        title="Transaction Amount Over Time"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Total Amount",
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# PAYMENT METHOD ANALYSIS
# =========================================================

st.subheader("Payment Method Analysis")

payment_summary = (
    filtered_df
    .groupby("Payment_Method")
    .agg(
        Transactions=("Transaction_ID", "count"),
        Total_Amount=("Transaction_Amount", "sum"),
        Average_Amount=("Transaction_Amount", "mean")
    )
    .reset_index()
    .sort_values(
        "Total_Amount",
        ascending=False
    )
)


col1, col2 = st.columns(2)

with col1:

    fig = px.bar(
        payment_summary,
        x="Payment_Method",
        y="Transactions",
        title="Transactions by Payment Method",
        text_auto=True
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Payment Method",
        yaxis_title="Transactions"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    fig = px.pie(
        payment_summary,
        names="Payment_Method",
        values="Total_Amount",
        title="Transaction Amount by Payment Method"
    )

    fig.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


st.dataframe(
    payment_summary,
    use_container_width=True
)


# =========================================================
# TRANSACTION CHANNEL ANALYSIS
# =========================================================

st.subheader("Transaction Channel Analysis")

channel_summary = (
    filtered_df
    .groupby("Transaction_Channel")
    .agg(
        Transactions=("Transaction_ID", "count"),
        Total_Amount=("Transaction_Amount", "sum"),
        Average_Amount=("Transaction_Amount", "mean")
    )
    .reset_index()
)


fig = px.bar(
    channel_summary,
    x="Transaction_Channel",
    y="Total_Amount",
    title="Total Transaction Amount by Channel",
    text_auto=".2s"
)

fig.update_layout(
    template="plotly_white",
    xaxis_title="Transaction Channel",
    yaxis_title="Total Amount"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# CURRENCY ANALYSIS
# =========================================================

st.subheader("Currency Analysis")

currency_summary = (
    filtered_df
    .groupby("Currency")
    .agg(
        Transactions=("Transaction_ID", "count"),
        Total_Amount=("Transaction_Amount", "sum"),
        Average_Amount=("Transaction_Amount", "mean")
    )
    .reset_index()
)


col1, col2 = st.columns(2)

with col1:

    fig = px.bar(
        currency_summary,
        x="Currency",
        y="Transactions",
        title="Transactions by Currency",
        text_auto=True
    )

    fig.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    fig = px.pie(
        currency_summary,
        names="Currency",
        values="Total_Amount",
        title="Transaction Amount by Currency"
    )

    fig.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# FRAUD ANALYSIS
# =========================================================

st.subheader("Fraud Analysis")

fraud_summary = (
    filtered_df
    .groupby("Fraud_Status")
    .agg(
        Transactions=("Transaction_ID", "count"),
        Total_Amount=("Transaction_Amount", "sum"),
        Average_Risk=("Risk_Score", "mean")
    )
    .reset_index()
)


col1, col2 = st.columns(2)

with col1:

    fig = px.pie(
        fraud_summary,
        names="Fraud_Status",
        values="Transactions",
        title="Legitimate vs Fraud Transactions"
    )

    fig.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    fig = px.bar(
        fraud_summary,
        x="Fraud_Status",
        y="Total_Amount",
        title="Transaction Amount: Fraud vs Legitimate",
        text_auto=".2s"
    )

    fig.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# RISK ANALYSIS
# =========================================================

st.subheader("Risk Score Analysis")

col1, col2 = st.columns(2)

with col1:

    fig = px.histogram(
        filtered_df,
        x="Risk_Score",
        nbins=20,
        title="Risk Score Distribution"
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Risk Score",
        yaxis_title="Number of Transactions"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    risk_summary = (
        filtered_df
        .groupby("Risk_Level", observed=True)
        .agg(
            Transactions=("Transaction_ID", "count"),
            Average_Amount=("Transaction_Amount", "mean"),
            Average_Risk=("Risk_Score", "mean")
        )
        .reset_index()
    )

    fig = px.bar(
        risk_summary,
        x="Risk_Level",
        y="Transactions",
        title="Transactions by Risk Level",
        text_auto=True
    )

    fig.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


st.dataframe(
    risk_summary,
    use_container_width=True
)


# =========================================================
# AGE ANALYSIS
# =========================================================

st.subheader("Customer Age Analysis")

col1, col2 = st.columns(2)

with col1:

    fig = px.histogram(
        filtered_df,
        x="Customer_Age",
        nbins=30,
        title="Customer Age Distribution"
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Customer Age",
        yaxis_title="Number of Customers"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    age_summary = (
        filtered_df
        .groupby("Customer_Age")
        .agg(
            Transactions=("Transaction_ID", "count"),
            Total_Amount=("Transaction_Amount", "sum"),
            Average_Amount=("Transaction_Amount", "mean")
        )
        .reset_index()
    )

    fig = px.line(
        age_summary,
        x="Customer_Age",
        y="Average_Amount",
        markers=True,
        title="Average Transaction Amount by Age"
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Customer Age",
        yaxis_title="Average Transaction Amount"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# TRANSACTION AMOUNT DISTRIBUTION
# =========================================================

st.subheader("Transaction Amount Analysis")

col1, col2 = st.columns(2)

with col1:

    fig = px.histogram(
        filtered_df,
        x="Transaction_Amount",
        nbins=50,
        title="Transaction Amount Distribution"
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Transaction Amount",
        yaxis_title="Number of Transactions"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    fig = px.box(
        filtered_df,
        y="Transaction_Amount",
        title="Transaction Amount Box Plot"
    )

    fig.update_layout(
        template="plotly_white",
        yaxis_title="Transaction Amount"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# AMOUNT VS RISK SCORE
# =========================================================

st.subheader("Transaction Amount vs Risk Score")

sample_df = filtered_df.sample(
    min(5000, len(filtered_df)),
    random_state=42
)

fig = px.scatter(
    sample_df,
    x="Risk_Score",
    y="Transaction_Amount",
    color="Fraud_Status",
    size="Transaction_Amount",
    hover_data=[
        "Transaction_ID",
        "Customer_ID",
        "Customer_Age",
        "Payment_Method",
        "Transaction_Channel",
        "Currency"
    ],
    title="Risk Score vs Transaction Amount"
)

fig.update_layout(
    template="plotly_white",
    xaxis_title="Risk Score",
    yaxis_title="Transaction Amount"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# CUSTOMER ANALYSIS
# =========================================================

st.subheader("Customer Analysis")

customer_summary = (
    filtered_df
    .groupby("Customer_ID")
    .agg(
        Transactions=("Transaction_ID", "count"),
        Total_Spending=("Transaction_Amount", "sum"),
        Average_Transaction=("Transaction_Amount", "mean"),
        Average_Risk=("Risk_Score", "mean")
    )
    .reset_index()
    .sort_values(
        "Total_Spending",
        ascending=False
    )
)


col1, col2 = st.columns(2)

with col1:

    fig = px.bar(
        customer_summary.head(10),
        x="Customer_ID",
        y="Total_Spending",
        title="Top 10 Customers by Total Spending",
        text_auto=".2s"
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Customer ID",
        yaxis_title="Total Spending"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    fig = px.scatter(
        customer_summary,
        x="Transactions",
        y="Total_Spending",
        size="Average_Transaction",
        hover_data=[
            "Customer_ID",
            "Average_Risk"
        ],
        title="Customer Transactions vs Total Spending"
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Number of Transactions",
        yaxis_title="Total Spending"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# YEARLY ANALYSIS
# =========================================================

st.subheader("Yearly Transaction Analysis")

yearly_summary = (
    filtered_df
    .groupby("Year")
    .agg(
        Transactions=("Transaction_ID", "count"),
        Total_Amount=("Transaction_Amount", "sum"),
        Average_Amount=("Transaction_Amount", "mean"),
        Fraud_Transactions=("Fraud_Flag", "sum")
    )
    .reset_index()
)

yearly_summary["Fraud_Rate"] = (
    yearly_summary["Fraud_Transactions"]
    /
    yearly_summary["Transactions"]
    * 100
)


fig = px.bar(
    yearly_summary,
    x="Year",
    y="Total_Amount",
    title="Total Transaction Amount by Year",
    text_auto=".2s"
)

fig.update_layout(
    template="plotly_white",
    xaxis_title="Year",
    yaxis_title="Total Transaction Amount"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(
    yearly_summary,
    use_container_width=True
)


# =========================================================
# DATASET SUMMARY
# =========================================================

st.subheader("Filtered Dataset")

st.write(
    f"Showing {len(filtered_df):,} transactions "
    f"out of {len(df):,} total transactions."
)

st.dataframe(
    filtered_df.head(100),
    use_container_width=True
)


# =========================================================
# DOWNLOAD DATA
# =========================================================

st.subheader("Download Data")

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Filtered Dataset",
    data=csv_data,
    file_name="filtered_financial_transactions.csv",
    mime="text/csv"
)


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "Financial Transactions Dashboard | "
    "Built with Streamlit, NumPy, Pandas and Plotly"
)