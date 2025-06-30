import streamlit as st
import pandas as pd

st.set_page_config(page_title="SmartSpend 💸", layout="centered")
st.title("💰 SmartSpend - Personal Finance Dashboard")

st.info("Welcome! Upload your bank statement (CSV) to get started.")

# Add download button for sample CSV
try:
    with open("src/assets/sample_statement.csv", "rb") as f:
        st.download_button("Download Sample CSV", f, file_name="sample_statement.csv")
except FileNotFoundError:
    st.warning("Sample CSV not found. Please add 'sample_statement.csv' to src/assets/ for the download button.")

uploaded_file = st.file_uploader("Upload Transactions File (CSV)", type=["csv"])
if uploaded_file:
    try:
        # Read CSV into DataFrame
        df = pd.read_csv(uploaded_file)
        required_columns = {'date', 'description', 'amount', 'type'}
        # Normalize column names
        df.columns = [c.strip().lower() for c in df.columns]
        missing = required_columns - set(df.columns)
        if missing:
            st.error(f"Missing required columns: {', '.join(missing)}.")
            st.stop()

        # Convert date and amount
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

        # Drop rows with missing critical info
        df.dropna(subset=['date', 'amount'], inplace=True)

        if df.empty:
            st.error("No valid transactions found after cleaning. Please check your file.")
            st.stop()

        st.success("File uploaded and cleaned successfully!")
        st.write("Here’s a preview of your cleaned data:")
        st.dataframe(df.head())

        # === BASIC SUMMARY ANALYTICS ===
        st.subheader("📊 Summary Statistics")
        total_income = df[df['type'].str.lower() == 'credit']['amount'].sum()
        total_expense = df[df['type'].str.lower() == 'debit']['amount'].sum()
        num_transactions = len(df)

        col1, col2, col3 = st.columns(3)
        col1.metric("💼 Income", f"SAR {total_income:,.2f}")
        col2.metric("💳 Expenses", f"SAR {total_expense:,.2f}")
        col3.metric("📈 Transactions", num_transactions)

    except Exception as e:
        st.error(f"An error occurred while reading your file: {e}")
        st.stop()
else:
    st.warning("📂 Please upload a CSV file to continue.")
