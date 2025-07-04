# SmartSpend: Saudi Bank Edition

SmartSpend is a comprehensive bilingual (Arabic/English) personal finance dashboard specifically designed for Saudi Arabian bank customers. The application empowers users to take control of their finances by uploading bank statements (CSV or PDF), automatically categorizing transactions, analyzing spending patterns, detecting recurring payments, and providing actionable financial insights.

[![SmartSpend Demo](https://img.shields.io/badge/View-Demo-blue)](https://github.com/Malekdevhub)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📸 Screenshots

<!-- Place your screenshots in the /screenshots folder and update the links below -->
![Dashboard](screenshots/dashboard_summary.png)
![Upload Accounts](screenshots/upload_multi_account.png)
![Edit Categories](screenshots/edit_categories_insights.png)
![Insights](screenshots/insights.png)
![Charts](screenshots/charts.png)

---

## 🚀 Features

### Core Functionality
- **Bilingual Support**: Full Arabic and English UI with one-click language switching
- **Multi-account Management**: Upload and analyze multiple bank accounts and credit cards together
- **Statement Processing**: Support for CSV and PDF formats from major Saudi banks
- **Data Export**: Download cleaned and categorized data as CSV or Excel files
- **Privacy-focused**: All data is processed locally - no server uploads

### Financial Analysis
- **Smart Categorization**: 
  - Automatic transaction categorization based on keywords
  - User-editable categorization rules
  - Default categories optimized for Saudi spending patterns
- **Recurring Payments**:
  - Automatic detection of monthly subscriptions and bills
  - Identification of potentially unused recurring payments
- **Visual Analytics**:
  - Expenses by category breakdown
  - Top 10 expenses analysis
  - Monthly spending trends
  - Next month spending predictions

### Financial Planning
- **Savings Goals**: Set and track monthly savings targets
- **Smart Insights**: Receive actionable tips to optimize spending
- **Spending Predictions**: ML-based forecasting of next month's expenses by category

---

## 🛠️ Requirements

- Python 3.7+
- Streamlit 1.10+
- pandas
- matplotlib
- pdfplumber
- numpy
- openpyxl (for Excel export)

## 🏁 Quickstart

1. **Clone the repository**
    ```bash
    git clone https://github.com/Malekdevhub/smartspend.git
    cd smartspend
    ```

2. **Install requirements**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the app**
    ```bash
    streamlit run app.py
    ```

4. **Access the dashboard**
    Open your browser and navigate to http://localhost:8501

5. **Upload your bank statement(s)**
    - Use the file upload section to import CSV or PDF files
    - Label each account (e.g., "Riyad Bank", "SABB Card")
    - Click "Process Accounts" to analyze your data

---

## 📚 Usage Guide

### Statement Format Support
The dashboard can handle various statement formats:
- CSV files with date, description, and amount columns
- PDF bank statements from major Saudi banks
- Multiple account statements simultaneously

### Customizing Categories
1. Use the sidebar to edit categorization rules
2. Add new categories or modify existing ones
3. Enter keywords (separated by commas) that identify each category
4. Changes apply immediately to your data

### Setting Financial Goals
1. Enter your monthly savings goal in SAR
2. The dashboard will analyze if you're on track
3. Receive suggestions based on your spending patterns

### Viewing Insights
The "Smart Insights & Suggestions" section provides:
- Month-over-month spending comparisons
- Identification of categories with significant increases
- Detection of potentially unused subscriptions
- Savings goal progress tracking

---

## 📂 Project Structure
smartspend/
├── app.py               # Main application entry point
├── smartspend_dashboard.py  # Dashboard implementation
├── README.md            # Project documentation
├── requirements.txt     # Python dependencies
│
├── /screenshots/        # Placeholder for application screenshots
│   └── .gitkeep
│
└── /src/
    └── /assets/
        ├── sample_statement.csv  # Sample data for demo
        └── .gitkeep
        

---

## 🔮 Future Development

- [ ] Automated categorization using machine learning
- [ ] Enhanced PDF parsing for additional bank formats
- [ ] Budget setting and tracking
- [ ] Data persistence to avoid re-uploading statements
- [ ] Mobile application version
- [ ] Shariah-compliant investment tracking
- [ ] Integration with Saudi payment systems

---

## 🏆 Why SmartSpend?

- **Localized**: Built specifically for Saudi banks and financial services
- **Bilingual**: Full Arabic and English support
- **Privacy-First**: All data processed locally on your device
- **Comprehensive**: Complete financial analysis in a user-friendly package
- **Customizable**: Adapt the system to your specific needs
- **Modern UI**: Clean, responsive design that works on any device

---

## ❓ Troubleshooting

**Q: My PDF statement isn't parsing correctly**  
A: Different banks format their PDFs differently. If you encounter issues, try exporting your statement as CSV instead.

**Q: Some transactions are incorrectly categorized**  
A: Use the category editor in the sidebar to add relevant keywords for your specific transactions.

**Q: The app is slow with large statements**  
A: For optimal performance, limit statements to the last 6 months of transactions.

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📞 Contact

- Author: Malekdevhub
- GitHub: [Malekdevhub](https://github.com/Malekdevhub)
- Email: [Add your email here]

---

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [pdfplumber](https://github.com/jsvine/pdfplumber) for PDF parsing capabilities
- Saudi banking community for testing and feedback
