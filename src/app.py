import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import pdfplumber
import re
import numpy as np

# --- THEME COLORS ---
PRIMARY_COLOR = "#21504b"
ACCENT_GREEN = "#007236"
ACCENT_BLUE = "#004990"
ACCENT_BROWN = "#4B2E06"
BG_DARK = "#181C1B"
LIGHT_SURFACE = "#F3F7F6"
TEXT_COLOR = "#ffffff"

st.set_page_config(page_title="SmartSpend: Saudi Bank Edition", layout="wide")

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {BG_DARK};
        color: {TEXT_COLOR};
    }}
    .stProgress > div > div > div {{
        background-image: linear-gradient(90deg, {PRIMARY_COLOR}, {ACCENT_GREEN}, {ACCENT_BLUE});
    }}
    .stNumberInput input {{
        background-color: {LIGHT_SURFACE};
        color: {BG_DARK};
    }}
    .stDataFrame {{background-color: {LIGHT_SURFACE}; color: {BG_DARK};}}
    .css-1kyxreq {{
        background-color: {PRIMARY_COLOR} !important;
        color: {TEXT_COLOR} !important;
    }}
    .css-1v0mbdj, .css-1d391kg {{
        background-color: {ACCENT_GREEN} !important;
    }}
    .stButton>button {{
        background-color: {PRIMARY_COLOR};
        color: {TEXT_COLOR};
        border: none;
        border-radius: 8px;
        padding: 0.5em 1.5em;
        margin-top: 0.5em;
    }}
    .stButton>button:hover {{
        background-color: {ACCENT_GREEN};
        color: {TEXT_COLOR};
    }}
    .css-2trqyj, .css-6qob1r {{
        background-color: {ACCENT_BROWN} !important;
    }}
    </style>
    """, unsafe_allow_html=True
)

# === Helper Functions ===

def get_language_labels(lang="en"):
    return {
        "en": {
            "dashboard_title": "💰 SmartSpend - Personal Finance Dashboard",
            "welcome": "Welcome! Upload your bank statement (CSV or PDF) to get started.",
            "download_sample": "Download Sample CSV",
            "upload_prompt": "Upload Transactions File (CSV or PDF)",
            "summary": "📊 Summary Statistics",
            "income": "💼 Income",
            "expense": "💳 Expenses",
            "transactions": "📈 Transactions",
            "category_chart": "📊 Expenses by Category",
            "top_expenses": "📂 Top 10 Expenses by Description",
            "monthly_trend": "📉 Monthly Spending Trend",
            "data_preview": "Here’s a preview of your cleaned and categorized data:",
            "edit_rules": "Edit Category Rules",
            "category_name": "Category name",
            "keywords": "Keywords (comma separated)",
            "add_category": "Add New Category",
            "reset_defaults": "Reset to Defaults",
            "file_error": "No valid transactions found after cleaning. Please check your file.",
            "upload_file": "📂 Please upload a CSV or PDF file to continue.",
            "lang_toggle": "Language",
            "success": "File uploaded and cleaned successfully!",
            "export_csv": "Download as CSV",
            "export_excel": "Download as Excel",
            "recurring": "Recurring?",
            "is_recurring": "Recurring",
            "not_recurring": "One-off",
            "recurring_note": "🔁 The following transactions are detected as recurring (subscriptions, bills, etc):",
            "insights": "💡 Smart Insights & Suggestions",
            "goal_input": "Set your monthly savings goal (SAR):",
            "on_track": "You are on track to meet your savings goal! 🎯",
            "off_track": "Warning: Your projected expenses may exceed your savings goal. ⚠️",
            "category_tip": "You spent {percent}% more on {cat} this month vs. last month.",
            "unused_recur": "You have a recurring payment for '{desc}' not used in the last 3 months. Consider cancelling.",
            "no_recurring_unused": "No unused recurring payments detected.",
            "set_goal": "Set Goal",
            "reset_goal": "Reset Goal",
            "multi_account_header": "🏦 Multi-Account & Card Aggregation",
            "multi_account_upload_label": "Upload one or more bank statements (CSV or PDF). For each, enter a label (e.g. 'Riyad Bank', 'SABB Card').",
            "account_label": "Label for file {i} ({fname})",
            "process_accounts": "Process Accounts",
            "show_data_for": "Show data for:",
            "all_accounts": "All accounts",
            "predicted_spending_header": "🔮 Predicted Spending Next Month"
        },
        "ar": {
            "dashboard_title": "لوحة تحكم سمارت سبيند 💰",
            "welcome": "مرحبًا! قم برفع كشف الحساب البنكي (CSV أو PDF) للبدء.",
            "download_sample": "تحميل ملف CSV تجريبي",
            "upload_prompt": "ارفع ملف العمليات البنكية (CSV أو PDF)",
            "summary": "📊 ملخص إحصائيات",
            "income": "💼 الدخل",
            "expense": "💳 المصروفات",
            "transactions": "📈 العمليات",
            "category_chart": "📊 المصروفات حسب التصنيف",
            "top_expenses": "📂 أعلى 10 مصروفات حسب الوصف",
            "monthly_trend": "📉 الاتجاه الشهري للمصروفات",
            "data_preview": "عرض أولي للبيانات بعد التنظيف والتصنيف:",
            "edit_rules": "تعديل تصنيفات العمليات",
            "category_name": "اسم التصنيف",
            "keywords": "كلمات مفتاحية (مفصولة بفاصلة)",
            "add_category": "إضافة تصنيف جديد",
            "reset_defaults": "إعادة التصنيفات الافتراضية",
            "file_error": "لا توجد عمليات صالحة بعد التنظيف. تحقق من الملف.",
            "upload_file": "📂 الرجاء رفع ملف CSV أو PDF للمتابعة.",
            "lang_toggle": "اللغة",
            "success": "تم رفع وتنظيف الملف بنجاح!",
            "export_csv": "تحميل كـ CSV",
            "export_excel": "تحميل كـ Excel",
            "recurring": "متكرر؟",
            "is_recurring": "متكرر",
            "not_recurring": "مرة واحدة",
            "recurring_note": "🔁 العمليات التالية تم اكتشافها كمدفوعات متكررة (اشتراكات، فواتير، إلخ):",
            "insights": "💡 اقتراحات ذكية",
            "goal_input": "حدد هدف الادخار الشهري (ريال):",
            "on_track": "أنت على المسار الصحيح لتحقيق هدف الادخار! 🎯",
            "off_track": "تحذير: من المتوقع أن تتجاوز المصروفات هدف الادخار. ⚠️",
            "category_tip": "أنفقت {percent}% أكثر على {cat} هذا الشهر مقارنة بالشهر الماضي.",
            "unused_recur": "لديك دفعة متكررة لـ '{desc}' لم تُستخدم خلال آخر ٣ أشهر. فكر في إلغائها.",
            "no_recurring_unused": "لا توجد مدفوعات متكررة غير مستخدمة.",
            "set_goal": "تعيين الهدف",
            "reset_goal": "إعادة تعيين الهدف",
            "multi_account_header": "🏦 تجميع الحسابات والبطاقات المتعددة",
            "multi_account_upload_label": "ارفع كشف حساب أو أكثر (CSV أو PDF). لكل واحد، أدخل تسمية (مثلاً 'بنك الرياض'، 'بطاقة ساب').",
            "account_label": "تسمية للملف {i} ({fname})",
            "process_accounts": "معالجة الحسابات",
            "show_data_for": "عرض بيانات:",
            "all_accounts": "كل الحسابات",
            "predicted_spending_header": "🔮 التنبؤ بالمصروفات الشهر القادم"
        }
    }[lang]

def get_default_rules():
    return [
        {"category_en": "Groceries", "category_ar": "البقالة", "keywords": "supermarket,grocery,market,store,mart,بقالة,سوبرماركت,ماركت"},
        {"category_en": "Restaurants & Cafes", "category_ar": "مطاعم ومقاهي", "keywords": "restaurant,cafe,coffee,burger,pizza,shawarma,مطعم,مقهى,قهوة,بيتزا,شاورما,برجر"},
        {"category_en": "Income", "category_ar": "الدخل", "keywords": "salary,payroll,income,deposit,راتب,دخل,ايداع"},
        {"category_en": "Cash", "category_ar": "سحب نقدي", "keywords": "atm,withdrawal,cash,سحب,صراف"},
        {"category_en": "Transport", "category_ar": "المواصلات", "keywords": "uber,taxi,lyft,ride,كريم,اوبر,تاكسي,مواصلات"},
        {"category_en": "Utilities", "category_ar": "خدمات", "keywords": "electric,water,utility,stc,mobily,zain,كهرباء,ماء,اتصالات,stc,موبايلي,زين,فاتورة"},
        {"category_en": "Transfers", "category_ar": "تحويلات", "keywords": "transfer,remittance,wire,تحويل,حوالة,إرسالية"},
        {"category_en": "Other", "category_ar": "أخرى", "keywords": ""},
    ]

def categorize(desc, rules):
    desc = str(desc).lower()
    for rule in rules:
        keywords = [k.strip() for k in rule["keywords"].split(",") if k.strip()]
        if any(k in desc for k in keywords):
            return rule
    return {"category_en": "Other", "category_ar": "أخرى", "keywords": ""}

def extract_pdf_table(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        dfs = []
        for page_num, page in enumerate(pdf.pages):
            table = page.extract_table()
            if table:
                df_page = pd.DataFrame(table[1:], columns=table[0])
                dfs.append(df_page)
        if dfs:
            return pd.concat(dfs, ignore_index=True)
        return pd.DataFrame()

def detect_recurring(df):
    df = df.copy()
    df['is_recurring'] = False
    group = df.groupby('description')
    for name, g in group:
        if len(g) < 3:
            continue
        g = g.sort_values('date')
        intervals = g['date'].diff().dt.days.dropna()
        if (intervals.between(27, 33).mean() > 0.7):
            idxs = g.index
            df.loc[idxs, 'is_recurring'] = True
    return df

def smart_insights(df, lang, labels, session_state):
    insights = []
    today = pd.Timestamp.today()
    df = df.copy()
    df['month'] = df['date'].dt.to_period('M')
    expense_df = df[df['type'].str.lower() == 'debit']

    this_month = today.to_period('M')
    last_month = (today - pd.DateOffset(months=1)).to_period('M')
    this_m = expense_df[expense_df['month'] == this_month]
    last_m = expense_df[expense_df['month'] == last_month]
    cats = df['category'].unique()
    for cat in cats:
        this_val = this_m[this_m['category'] == cat]['amount'].sum()
        last_val = last_m[last_m['category'] == cat]['amount'].sum()
        if last_val > 0 and this_val > last_val * 1.15:
            percent = int(100 * (this_val - last_val) / last_val)
            insights.append(labels["category_tip"].format(percent=percent, cat=cat))

    recent_3m = (today - pd.DateOffset(months=3)).to_period('M')
    recurring = df[df['is_recurring']]
    unused = []
    for desc in recurring['description'].unique():
        desc_df = recurring[recurring['description'] == desc]
        if desc_df['month'].max() < recent_3m:
            unused.append(desc)
    if unused:
        for desc in unused:
            insights.append(labels["unused_recur"].format(desc=desc))
    else:
        insights.append(labels["no_recurring_unused"])

    if "goal" in session_state and session_state["goal"]:
        this_month_income = df[(df['type'].str.lower() == 'credit') & (df['month'] == this_month)]['amount'].sum()
        this_month_expense = expense_df[expense_df['month'] == this_month]['amount'].sum()
        savings = this_month_income - this_month_expense
        if savings >= session_state["goal"]:
            insights.append(labels["on_track"])
        else:
            insights.append(labels["off_track"])

    return insights

def predict_next_month(expense_df):
    if expense_df.empty:
        return pd.DataFrame()
    expense_df = expense_df.copy()
    expense_df['month'] = expense_df['date'].dt.to_period('M')
    last_month = expense_df['month'].max()
    categories = expense_df['category'].unique()
    preds = []
    for cat in categories:
        cat_data = expense_df[expense_df['category'] == cat]
        last3 = cat_data[cat_data['month'] >= (last_month - 2)]
        avg = last3['amount'].abs().mean()
        preds.append({'category': cat, 'predicted': avg if not np.isnan(avg) else 0})
    return pd.DataFrame(preds)

def process_uploaded_file(file, label):
    def make_unique_columns(cols):
        seen = {}
        result = []
        for col in cols:
            if col not in seen:
                seen[col] = 0
                result.append(col)
            else:
                seen[col] += 1
                result.append(f"{col}_{seen[col]}")
        return result

    if file.name.lower().endswith(".csv"):
        df = pd.read_csv(file)
    elif file.name.lower().endswith(".pdf"):
        pdf_df = extract_pdf_table(file)
        st.write("**Extracted columns:**", list(pdf_df.columns))
        st.dataframe(pdf_df.head())
        pdf_df.columns = [c.lower().strip() for c in pdf_df.columns]
        rename_map = {}
        for c in pdf_df.columns:
            if re.search(r"date|تاريخ|تاريخ القيد", c, re.I): rename_map[c] = "date"
            if re.search(r"desc|statement|بيان|وصف|وصف العملية", c, re.I): rename_map[c] = "description"
            if re.search(r"amount|مبلغ|المبلغ", c, re.I): rename_map[c] = "amount"
            if re.search(r"debit|مدين", c, re.I): rename_map[c] = "debit"
            if re.search(r"credit|دائن", c, re.I): rename_map[c] = "credit"
        pdf_df = pdf_df.rename(columns=rename_map)
        pdf_df.columns = make_unique_columns(pdf_df.columns)
        df = pdf_df
    else:
        return pd.DataFrame()
    df.columns = [c.strip().lower() for c in df.columns]

    col_date = next((col for col in df.columns if col.startswith('date')), None)
    col_desc = next((col for col in df.columns if col.startswith('description')), None)
    col_amount = next((col for col in df.columns if col.startswith('amount')), None)

    debit_col = next((col for col in df.columns if col.startswith('debit')), None)
    credit_col = next((col for col in df.columns if col.startswith('credit')), None)

    if (debit_col or credit_col):
        df['amount'] = (
            pd.to_numeric(df[credit_col], errors='coerce').fillna(0) if credit_col else 0
        ) - (
            pd.to_numeric(df[debit_col], errors='coerce').fillna(0) if debit_col else 0
        )
        col_amount = 'amount'
    elif col_amount:
        df[col_amount] = pd.to_numeric(df[col_amount], errors='coerce')
    else:
        st.error("No amount, debit, or credit columns found.")
        return pd.DataFrame()

    if 'type' not in df.columns:
        df['type'] = np.where(df[col_amount] >= 0, 'credit', 'debit')

    required = [col_date, col_desc, col_amount, 'type']
    if not all(required):
        st.error(f"**Required columns not found:** {[c for c in ['date','description','amount','type'] if c not in required]}")
        return pd.DataFrame()

    df['date'] = pd.to_datetime(df[col_date], errors='coerce')
    df['description'] = df[col_desc]
    df['amount'] = df[col_amount]
    df = df[['date', 'description', 'amount', 'type']]
    df.dropna(subset=['date', 'amount'], inplace=True)
    df["Account"] = label
    return df

# === Streamlit App Start ===

lang = st.sidebar.selectbox(
    "Language | اللغة",
    options=[("English", "en"), ("العربية", "ar")],
    format_func=lambda x: x[0],
    index=0
)[1]
labels = get_language_labels(lang)

st.title(labels["dashboard_title"])
st.info(labels["welcome"])

try:
    with open("src/assets/sample_statement.csv", "rb") as f:
        st.download_button(labels["download_sample"], f, file_name="sample_statement.csv")
except FileNotFoundError:
    st.warning("Sample CSV not found. Please add 'sample_statement.csv' to src/assets/ for the download button.")

st.header(labels["multi_account_header"])
uploaded_files = st.file_uploader(
    labels["multi_account_upload_label"],
    accept_multiple_files=True,
    type=["csv", "pdf"]
)

dfs = []
file_labels = []
if uploaded_files:
    st.write("Assign a label to each file:")
    for i, file in enumerate(uploaded_files):
        label = st.text_input(
            labels["account_label"].format(i=i+1, fname=file.name),
            value=f"Account{i+1}",
            key=f"label_{i}"
        )
        file_labels.append(label)
    if st.button(labels["process_accounts"]):
        for file, label in zip(uploaded_files, file_labels):
            df1 = process_uploaded_file(file, label)
            if df1.empty:
                st.warning(f"File '{file.name}' is missing required columns or no data after cleaning.")
            else:
                dfs.append(df1)
        if not dfs:
            st.error("No valid data found in uploaded files.")
        else:
            df = pd.concat(dfs, ignore_index=True)
else:
    df = None

if 'df' not in locals():
    df = None

if df is not None and not df.empty:
    st.sidebar.header(labels["edit_rules"])
    if "rules" not in st.session_state:
        st.session_state["rules"] = get_default_rules()
    rules = st.session_state["rules"]

    for i, rule in enumerate(rules):
        col1, col2, col3 = st.sidebar.columns([2,2,4])
        rules[i]["category_en"] = col1.text_input(f"EN {labels['category_name']} {i+1}", value=rule["category_en"], key=f"cat_en_{i}")
        rules[i]["category_ar"] = col2.text_input(f"AR {labels['category_name']} {i+1}", value=rule["category_ar"], key=f"cat_ar_{i}")
        rules[i]["keywords"] = col3.text_input(labels["keywords"], value=rule["keywords"], key=f"key_{i}")

    if st.sidebar.button(labels["add_category"]):
        rules.append({"category_en": f"NewCategory{len(rules)+1}", "category_ar": f"تصنيف{len(rules)+1}", "keywords": ""})

    if st.sidebar.button(labels["reset_defaults"]):
        st.session_state["rules"] = get_default_rules()
        st.rerun()

    df["_cat_obj"] = df["description"].apply(lambda x: categorize(x, rules))
    cat_col = "category_en" if lang == "en" else "category_ar"
    df['category'] = df["_cat_obj"].apply(lambda c: c[cat_col])

    df = detect_recurring(df)
    recurring_label = labels["is_recurring"]
    not_recurring_label = labels["not_recurring"]
    df[labels["recurring"]] = df["is_recurring"].map({True: recurring_label, False: not_recurring_label})

    account_options = [labels["all_accounts"]] + sorted(df["Account"].unique())
    selected_account = st.selectbox(labels["show_data_for"], options=account_options)
    df_filtered = df if selected_account == labels["all_accounts"] else df[df["Account"] == selected_account]

    df_filtered['month'] = df_filtered['date'].dt.to_period('M').astype(str)

    st.subheader(labels["insights"])
    if "goal" not in st.session_state:
        st.session_state["goal"] = None
    with st.form("goal_form", clear_on_submit=False):
        goal_input = st.number_input(
            labels["goal_input"],
            min_value=0, step=100, value=st.session_state["goal"] or 0, format="%d"
        )
        colg1, colg2 = st.columns(2)
        set_goal = colg1.form_submit_button(labels["set_goal"])
        reset_goal = colg2.form_submit_button(labels["reset_goal"])
        if set_goal:
            st.session_state["goal"] = int(goal_input)
        if reset_goal:
            st.session_state["goal"] = None
    insights = smart_insights(df_filtered, lang, labels, st.session_state)
    for tip in insights:
        st.info(tip)

    st.success(labels["success"])
    st.write(labels["data_preview"])
    st.dataframe(df_filtered.drop(columns=["_cat_obj"]).head())

    st.subheader(labels["predicted_spending_header"])
    expense_df = df_filtered[df_filtered['type'].str.lower() == 'debit']
    expense_df['month'] = expense_df['date'].dt.to_period('M').astype(str)
    pred_df = predict_next_month(expense_df)
    if not pred_df.empty:
        st.dataframe(pred_df.set_index("category"))
        if st.session_state.get("goal"):
            goal = st.session_state["goal"]
            total_pred = pred_df["predicted"].sum()
            if total_pred > goal:
                st.warning(f"⚠️ Predicted total expenses ({total_pred:,.0f} SAR) exceed your goal ({goal:,.0f} SAR).")
            else:
                st.success(f"🎯 Predicted total expenses ({total_pred:,.0f} SAR) are within your goal ({goal:,.0f} SAR).")
        fig, ax = plt.subplots(figsize=(8, 4))
        pred_df.set_index("category")["predicted"].plot(kind="bar", color=ACCENT_BLUE, ax=ax)
        ax.set_ylabel("Predicted Amount (SAR)")
        ax.set_title(labels["predicted_spending_header"])
        st.pyplot(fig)

    export_df = df_filtered.drop(columns=["_cat_obj"])
    col_csv, col_excel = st.columns(2)
    csv = export_df.to_csv(index=False).encode("utf-8")
    col_csv.download_button(
        label=labels["export_csv"],
        data=csv,
        file_name="smartspend_cleaned.csv",
        mime="text/csv"
    )
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
        export_df.to_excel(writer, index=False, sheet_name="SmartSpend")
    col_excel.download_button(
        label=labels["export_excel"],
        data=excel_buffer.getvalue(),
        file_name="smartspend_cleaned.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    recurring_df = export_df[export_df["is_recurring"]]
    if not recurring_df.empty:
        st.info(labels["recurring_note"])
        st.dataframe(recurring_df[["date", "description", "amount", "category", labels["recurring"]]])

    st.subheader(labels["summary"])
    total_income = df_filtered[df_filtered['type'].str.lower() == 'credit']['amount'].sum()
    total_expense = df_filtered[df_filtered['type'].str.lower() == 'debit']['amount'].sum()
    num_transactions = len(df_filtered)
    col1, col2, col3 = st.columns(3)
    col1.metric(labels["income"], f"SAR {total_income:,.2f}")
    col2.metric(labels["expense"], f"SAR {total_expense:,.2f}")
    col3.metric(labels["transactions"], num_transactions)

    st.subheader(labels["category_chart"])
    expense_df['month'] = expense_df['date'].dt.to_period('M').astype(str)
    cat_expenses = expense_df.groupby('category')['amount'].sum().abs().sort_values(ascending=False)
    st.bar_chart(cat_expenses, color=ACCENT_GREEN)

    st.subheader(labels["top_expenses"])
    top_expenses = expense_df.groupby('description')['amount'].sum().abs().sort_values(ascending=False).head(10)
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    top_expenses.plot(kind='barh', color=ACCENT_BROWN, ax=ax1)
    ax1.set_xlabel("Amount (SAR)")
    ax1.set_ylabel("Description" if lang=="en" else "الوصف")
    ax1.set_title(labels["top_expenses"])
    st.pyplot(fig1)

    st.subheader(labels["monthly_trend"])
    expense_df['month'] = expense_df['date'].dt.to_period('M').astype(str)
    monthly = expense_df.groupby('month')['amount'].sum().abs()
    st.line_chart(monthly, color=PRIMARY_COLOR)

else:
    st.warning(labels["upload_file"])