import streamlit as st
import pandas as pd

st.set_page_config(page_title="SmartSpend 💸", layout="centered")
st.title("💰 SmartSpend - Personal Finance Dashboard")

st.info("Welcome! Upload your bank statement (CSV) to get started.")

uploaded_file = st.file_uploader("Upload Transactions File (CSV)", type=["csv"])
if uploaded_file:
    # Read CSV into DataFrame
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully!")
    st.write("Here’s a preview of your data:")
    st.dataframe(df.head())
else:
    st.warning("📂 Please upload a CSV file to continue.")
