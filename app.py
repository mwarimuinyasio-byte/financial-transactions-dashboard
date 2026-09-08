import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Financial Transactions Dashboard",
    layout="wide"
)

st.title("Financial Transactions Data Analysis")

# Generate synthetic data
np.random.seed(42)

n = 100000

df = pd.DataFrame({
    "Transaction_ID": np.arange(1, n + 1),

    "Customer_ID": np.random.randint(
        1000, 10000, n
    ),

    "Customer_Age": np.random.randint(
        18, 70, n
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
            10, 10000, n
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
        ["KES", "USD", "EUR", "GBP"],
        n
    ),

    "Fraud_Flag": np.random.choice(
        [0, 1],
        n,
        p=[0.97, 0.03]
    ),

    "Risk_Score": np.random.randint(
        1, 101, n
    )
})

st.subheader("Synthetic Financial Transactions")

st.write("Number of records:", len(df))

st.dataframe(df.head(20))