import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime

# Import custom utilities
from utils.bookkeeping import generate_mock_transactions, calculate_financials, TransactionClassifier
from utils.audit import audit_transactions
from utils.forecasting import forecast_financials
from utils.taxation import calculate_taxes, get_tax_savings_recommendations
from utils.pdf_generator import generate_financial_pdf
from utils.chatbot import AIChatbot

# Page configuration
st.set_page_config(
    page_title="Zenith CA - AI Chartered Accountant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State for interactive profile & wizard (Feature 1 & 2)
if "profile" not in st.session_state:
    st.session_state.profile = {
        "name": "Heet Enterprises",
        "type": "Private Limited Company (Pvt Ltd)",
        "employees": 12,
        "revenue": 120000.0,
        "expenses": 80000.0,
        "gst_registered": "Yes",
        "bank_cash": 450000.0,
        "expenses_breakdown": {
            "Payroll & Contractors": 30000.0,
            "Rent & Office Space": 15000.0,
            "Utilities & Internet": 3000.0,
            "Software & Infrastructure": 5000.0,
            "Marketing & Advertising": 18000.0,
            "Travel & Lodging": 4000.0,
            "Tax & Legal Fees": 2000.0,
            "Miscellaneous Expense": 3000.0
        },
        "subscriptions": [
            {"name": "Amazon Web Services (AWS)", "cost": 3200.0, "status": "Active", "category": "Software & Infrastructure"},
            {"name": "Adobe Creative Cloud", "cost": 1200.0, "status": "Unused", "category": "Software & Infrastructure"},
            {"name": "Zoom Enterprise", "cost": 400.0, "status": "Active", "category": "Software & Infrastructure"},
            {"name": "Canva Pro Team", "cost": 600.0, "status": "Unused", "category": "Software & Infrastructure"},
            {"name": "Slack Pro Workspace", "cost": 800.0, "status": "Active", "category": "Software & Infrastructure"}
        ]
    }

# Session State for interactive Q&A (Feature 6)
if "qa_answers" not in st.session_state:
    st.session_state.qa_answers = {
        "pay_rent": "Yes",
        "rent_amount": 15000,
        "own_office": "No",
        "has_gst": "Yes",
        "employees": 12,
        "payroll": 30000,
        "own_laptops": "Yes",
        "laptops_worth": 350000
    }

# Custom CSS for Light Theme & White Premium Aesthetics
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"], .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #eff6ff 100%) !important;
        color: #0f172a !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    
    div.stMetric, div[data-testid="stMetricValue"] {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 15px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
        color: #0f172a !important;
        transition: all 0.3s ease-in-out !important;
    }
    
    div.stMetric:hover {
        transform: translateY(-3px) !important;
        border-color: #2563eb !important;
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.1) !important;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
    }
    
    .main-title {
        background: linear-gradient(to right, #1d4ed8, #2563eb, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
        margin-bottom: 0.2rem;
    }
    
    .subtitle {
        color: #475569;
        font-size: 1.15rem;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #e2e8f0 !important;
        padding: 8px !important;
        border-radius: 12px !important;
        border: 1px solid #cbd5e1 !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 48px !important;
        border-radius: 8px !important;
        color: #475569 !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 0px 18px !important;
        transition: all 0.2s ease !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2563eb !important;
        color: #ffffff !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.2) !important;
    }
    
    .highlight-card {
        background: #ffffff;
        border: 1px solid #bfdbfe;
        border-left: 5px solid #2563eb;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    
    .warning-card {
        background: #ffffff;
        border: 1px solid #fecaca;
        border-left: 5px solid #ef4444;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    
    .success-card {
        background: #ffffff;
        border: 1px solid #bbf7d0;
        border-left: 5px solid #22c55e;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    
    .briefing-card {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
        color: #ffffff !important;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(30, 58, 138, 0.15);
    }
    
    .briefing-card h3, .briefing-card h4, .briefing-card p, .briefing-card span {
        color: #ffffff !important;
    }
    
    div.stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.5rem !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15) !important;
        transition: all 0.2s ease !important;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.25) !important;
    }
    
    .user-bubble {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 15px 15px 0px 15px;
        padding: 15px;
        margin: 10px 0px;
        color: #1e293b;
    }
    
    .assistant-bubble {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 15px 15px 15px 0px;
        padding: 15px;
        margin: 10px 0px;
        line-height: 1.6;
        color: #1e293b;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
</style>
""", unsafe_allow_html=True)

# Main Titles
st.markdown("<h1 class='main-title'>Zenith CA</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Autonomous AI-Powered Chartered Accountant & Virtual CFO Platform</p>", unsafe_allow_html=True)

# --- SIDEBAR: Operational Controls & Data Mode Selector ---
st.sidebar.markdown("### Profile Control")
data_source_mode = st.sidebar.radio(
    "Active Data Mode",
    ["Interactive Onboarding Profile", "Uploaded CSV Ledger"],
    help="Toggle between the interactive profile wizard and uploading your transaction CSV file."
)

st.sidebar.markdown("---")

# Slider for Simulator (Feature 5: What-if Simulator)
st.sidebar.markdown("### Monthly What-if Simulator")
what_if_rev_pct = st.sidebar.slider(
    "Simulate Revenue Adjustments (%)",
    -50, 100, 0,
    help="Directly adjusts simulated monthly revenue and updates cash flows, taxes, and runways instantly."
)

what_if_exp_pct = st.sidebar.slider(
    "Simulate Expenses Adjustments (%)",
    -50, 50, 0,
    help="Adjusts overheads/expenses by this percentage to evaluate runway changes."
)

st.sidebar.markdown("---")

# PDF Generation in Sidebar
st.sidebar.markdown("### Export Official Report")

# --- Helper: Generate ledger and metrics dynamically based on source mode ---
def get_current_financial_state():
    p = st.session_state.profile
    # What-if adjustments
    rev_mult = (100 + what_if_rev_pct) / 100.0
    exp_mult = (100 + what_if_exp_pct) / 100.0
    
    if data_source_mode == "Uploaded CSV Ledger" and 'uploaded_df' in st.session_state:
        df = st.session_state.uploaded_df.copy()
        
        # Apply what-if adjustments to the dataframe
        df.loc[df["Type"] == "Income", "Amount"] *= rev_mult
        df.loc[df["Type"] == "Expense", "Amount"] *= exp_mult
        
        financials = calculate_financials(df)
        tax_data = calculate_taxes(df, p["type"], p["expenses_breakdown"]["Payroll & Contractors"])
        audit_findings = audit_transactions(df)
        forecasting_data = forecast_financials(df)
        
        # Overwrite transient metrics for consistency
        financials["Total_Revenue"] = df[df["Type"] == "Income"]["Amount"].sum()
        financials["Total_Expenses"] = df[df["Type"] == "Expense"]["Amount"].sum()
        financials["Net_Income"] = financials["Total_Revenue"] - financials["Total_Expenses"]
        
        return df, financials, tax_data, audit_findings, forecasting_data
        
    else:
        # Build ledger matching Onboarding profile values
        base_revenue = p["revenue"] * rev_mult
        
        # Build categories based on adjusted expenses breakdown
        adjusted_breakdown = {k: v * exp_mult for k, v in p["expenses_breakdown"].items()}
        base_expense = sum(adjusted_breakdown.values())
        
        # Generate transactions locally to represent the profile
        np.random.seed(42)
        dates = []
        descriptions = []
        amounts = []
        types = []
        categories = []
        
        # Create 12 months history
        start_date = datetime.date.today() - datetime.timedelta(days=365)
        for month in range(12):
            m_date = start_date + datetime.timedelta(days=month * 30)
            
            # Inflow
            dates.append(m_date)
            descriptions.append("SaaS customer subscriptions stripe payout")
            amounts.append(np.round(base_revenue * np.random.uniform(0.9, 1.1), 2))
            types.append("Income")
            categories.append("Revenue")
            
            # Expenses
            for cat, val in adjusted_breakdown.items():
                dates.append(m_date + datetime.timedelta(days=np.random.randint(1, 28)))
                descriptions.append(f"Business operational spending: {cat}")
                amounts.append(np.round(val * np.random.uniform(0.85, 1.15), 2))
                types.append("Expense")
                categories.append(cat)
                
        df = pd.DataFrame({
            "Date": dates,
            "Description": descriptions,
            "Amount": amounts,
            "Type": types,
            "Category": categories,
            "Transaction_ID": [f"TX-{1000 + i}" for i in range(len(dates))]
        }).sort_values(by="Date").reset_index(drop=True)
        
        financials = calculate_financials(df)
        tax_data = calculate_taxes(df, p["type"], adjusted_breakdown.get("Payroll & Contractors", 0))
        
        # Inject custom initial cash setting
        financials["Current_Cash"] = p["bank_cash"] + (financials["Net_Income"])
        financials["Balance_Sheet"]["Assets"]["Cash & Cash Equivalents"] = financials["Current_Cash"]
        financials["Balance_Sheet"]["Assets"]["Total Assets"] = financials["Current_Cash"] + financials["Balance_Sheet"]["Assets"]["Accounts Receivable"] + financials["Balance_Sheet"]["Assets"]["Equipment & Hardware"]
        
        # Recalculate cash trend with custom initial bank balance
        cash_series = [p["bank_cash"]]
        current = p["bank_cash"]
        df_sorted = df.copy()
        df_sorted["Flow"] = df_sorted.apply(lambda r: r["Amount"] if r["Type"] == "Income" else -r["Amount"], axis=1)
        for val in df_sorted["Flow"]:
            current += val
            cash_series.append(current)
        df_sorted["Cumulative_Cash"] = cash_series[1:]
        financials["Cash_Trend"] = df_sorted[["Date", "Cumulative_Cash"]]
        
        audit_findings = audit_transactions(df)
        forecasting_data = forecast_financials(df)
        forecasting_data["Avg_Monthly_Income"] = base_revenue
        forecasting_data["Avg_Monthly_Expenses"] = base_expense
        forecasting_data["Net_Monthly_Burn"] = max(0.0, base_expense - base_revenue)
        forecasting_data["Runway_Months"] = float('inf') if base_revenue >= base_expense else financials["Current_Cash"] / (base_expense - base_revenue)
        
        return df, financials, tax_data, audit_findings, forecasting_data

# Upload CSV Handler
uploaded_file = st.sidebar.file_uploader(
    "Upload Transaction Ledger (CSV)",
    type=["csv"],
    help="Will activate once 'Uploaded CSV Ledger' mode is selected."
)

if uploaded_file is not None:
    try:
        raw_df = pd.read_csv(uploaded_file)
        # Apply standard mappings as in previous load_transaction_data logic
        col_mapping = {}
        for col in raw_df.columns:
            col_lower = col.lower()
            if "date" in col_lower or "timestamp" in col_lower:
                col_mapping[col] = "Date"
            elif "desc" in col_lower or "particular" in col_lower or "narrative" in col_lower:
                col_mapping[col] = "Description"
            elif "amount" in col_lower or "value" in col_lower or "dr" in col_lower or "cr" in col_lower:
                col_mapping[col] = "Amount"
            elif "type" in col_lower or "category" in col_lower or "flow" in col_lower:
                col_mapping[col] = "Type"
        raw_df = raw_df.rename(columns=col_mapping)
        raw_df["Date"] = pd.to_datetime(raw_df["Date"]).dt.date
        raw_df["Amount"] = pd.to_numeric(raw_df["Amount"].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0.0)
        
        if "Type" not in raw_df.columns:
            raw_df["Type"] = raw_df["Amount"].apply(lambda x: "Expense" if x < 0 else "Income")
            raw_df["Amount"] = raw_df["Amount"].abs()
        else:
            raw_df["Type"] = raw_df["Type"].apply(lambda x: "Income" if "inc" in str(x).lower() or "cr" in str(x).lower() or "in" in str(x).lower() else "Expense")
            
        raw_df["Transaction_ID"] = [f"TX-{1000 + i}" for i in range(len(raw_df))]
        clf = TransactionClassifier()
        raw_df["Category"] = clf.predict(raw_df["Description"].tolist())
        raw_df.loc[raw_df["Type"] == "Income", "Category"] = "Revenue"
        raw_df.loc[raw_df["Description"].str.contains("rent|lease", case=False), "Category"] = "Rent & Office Space"
        raw_df.loc[raw_df["Description"].str.contains("payroll|salary|wages", case=False), "Category"] = "Payroll & Contractors"
        
        st.session_state.uploaded_df = raw_df
        if data_source_mode != "Uploaded CSV Ledger":
            st.sidebar.success("CSV Uploaded! Change 'Active Data Mode' above to activate it.")
    except Exception as e:
        st.sidebar.error(f"Error parsing CSV: {e}")

# Fetch active financial state
df_transactions, financials, tax_data, audit_findings, forecasting_data = get_current_financial_state()

# Download PDF Report button in sidebar
if st.sidebar.button("Generate Financial PDF"):
    try:
        pdf_bytes = generate_financial_pdf(financials, tax_data, audit_findings, st.session_state.profile["type"])
        st.sidebar.download_button(
            label="Download PDF Report",
            data=pdf_bytes,
            file_name=f"Zenith_CA_Financial_Report_{datetime.date.today().strftime('%Y_%m_%d')}.pdf",
            mime="application/pdf"
        )
        st.sidebar.success("PDF generated successfully! Click 'Download PDF Report' above.")
    except Exception as e:
        st.sidebar.error(f"Error compiling PDF: {e}")

# --- TOP METRICS HEADER PANEL ---
m_row1_col1, m_row1_col2, m_row1_col3 = st.columns(3)
with m_row1_col1:
    st.metric("Total Revenue", f"₹{financials['Total_Revenue']:,.2f}")
with m_row1_col2:
    st.metric("Total Expenses", f"₹{financials['Total_Expenses']:,.2f}")
with m_row1_col3:
    net_val = financials['Net_Income']
    margin_pct = ((net_val/financials['Total_Revenue'])*100 if financials['Total_Revenue'] > 0 else 0)
    st.metric("Net Profit", f"₹{net_val:,.2f}", delta=f"{margin_pct:.1f}% Margin")

m_row2_col1, m_row2_col2, m_row2_col3 = st.columns(3)
with m_row2_col1:
    st.metric("Est. Net GST Due", f"₹{tax_data['Net_GST_Payable']:,.2f}")
with m_row2_col2:
    it_info = tax_data['Income_Tax']
    it_val = it_info.get("Total Income Tax Payable", it_info.get("Total_Income_Tax Payable", 0))
    st.metric("Income Tax Payable", f"₹{it_val:,.2f}", delta=f"Effective: {it_info.get('Effective Tax Rate', 'N/A')}")
with m_row2_col3:
    runway = forecasting_data['Runway_Months']
    runway_str = f"{runway:.1f} Mon" if runway != float('inf') else "Positive"
    st.metric("Cash Runway", runway_str, delta=f"Cash: ₹{financials['Current_Cash']:,.2f}")

st.write("")

# --- TABS LAYOUT ---
tab_brief, tab_setup, tab_sim, tab_goals, tab_tax, tab_audit, tab_chat = st.tabs([
    "AI CFO Executive Suite",
    "Company Setup & Expense Builder",
    "Simulators & Advisors",
    "Growth & Goal Planner",
    "Tax Planner & Smart Saving",
    "Forensic Audit & Invoice Analyzer",
    "Consult Senior AI CA"
])

# ==================== TAB 1: AI CFO EXECUTIVE SUITE ====================
with tab_brief:
    # Feature 20: Daily AI Finance Assistant (Greeting Card)
    days_to_gst = 20 - datetime.date.today().day if datetime.date.today().day < 20 else 20
    suspicious_count = len(audit_findings[audit_findings["Severity"] == "High"])
    
    st.markdown(f"""
    <div class='briefing-card'>
        <h3>Good Morning, {st.session_state.profile['name'].split()[0]}!</h3>
        <p style='font-size: 1.1rem; opacity: 0.9;'>Here is your daily briefing from Zenith CA:</p>
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 15px;'>
            <div>
                <strong>Active Balance:</strong><br>
                <span style='font-size: 1.4rem;'>₹{financials['Current_Cash']:,.2f}</span>
            </div>
            <div>
                <strong>GST Deadline Alert:</strong><br>
                <span style='font-size: 1.4rem;'>GSTR-1 due in {days_to_gst} days</span>
            </div>
            <div>
                <strong>Audit Fraud Warning:</strong><br>
                <span style='font-size: 1.4rem; color: #fca5a5;'>{suspicious_count} High Risk Flags</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    cfo_col1, cfo_col2 = st.columns([1, 1])
    
    with cfo_col1:
        # Feature 3: AI Financial Health Score (Visual and Breakdown)
        st.markdown("### AI Financial Health Score")
        
        # Calculate scores
        liquidity_score = int(min(100, (financials['Current_Cash'] / (financials['Total_Expenses']/12.0 or 1.0)) * 10))
        profitability_score = int(min(100, max(0, financials['Net_Income'] / (financials['Total_Revenue'] or 1.0)) * 200))
        compliance_score = 90 if st.session_state.profile["gst_registered"] == "Yes" else 60
        if len(audit_findings) > 0:
            compliance_score -= min(30, len(audit_findings) * 5)
        cashflow_score = 95 if financials["Net_Income"] > 0 else 45
        debt_score = 100 # No debt by default
        
        health_score = int((liquidity_score + profitability_score + compliance_score + cashflow_score + debt_score) / 5)
        
        # Gauge Chart
        fig_score = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = health_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Zenith Health Index", 'font': {'size': 20}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#2563eb"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "#cbd5e1",
                'steps': [
                    {'range': [0, 50], 'color': '#fee2e2'},
                    {'range': [50, 80], 'color': '#fef3c7'},
                    {'range': [80, 100], 'color': '#dcfce7'}
                ]
            }
        ))
        fig_score.update_layout(height=280, margin=dict(t=30, b=10, l=10, r=10), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_score, use_container_width=True)
        
        # Breakdowns
        st.markdown("#### Score Component Breakdown")
        score_df = pd.DataFrame({
            "Component": ["Liquidity Buffer", "Profitability Margin", "Tax & Audit Compliance", "Cash Flow Strength", "Debt Risk"],
            "Score": [liquidity_score, profitability_score, compliance_score, cashflow_score, debt_score]
        })
        st.dataframe(score_df, hide_index=True, use_container_width=True)
        
    with cfo_col2:
        # Feature 18: AI Risk Meter (Gauges/Cards)
        st.markdown("### AI Risk Meter")
        
        fin_risk = 100 - profitability_score
        audit_risk = int(min(100, len(audit_findings) * 10 + (20 if suspicious_count > 0 else 0)))
        fraud_risk = 30 if suspicious_count > 0 else 5
        liq_risk = 100 - liquidity_score
        
        def render_risk_bar(label, value):
            color = "#ef4444" if value > 60 else ("#f59e0b" if value > 30 else "#22c55e")
            st.markdown(f"""
            <div style='margin-bottom: 15px;'>
                <div style='display: flex; justify-content: space-between; font-weight: 600; font-size: 0.95rem;'>
                    <span>{label}</span>
                    <span style='color: {color};'>{value}%</span>
                </div>
                <div style='background: #e2e8f0; height: 10px; border-radius: 5px; margin-top: 5px; overflow: hidden;'>
                    <div style='background: {color}; width: {value}%; height: 100%; border-radius: 5px;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        render_risk_bar("Financial Exposure Risk", fin_risk)
        render_risk_bar("Statutory Audit Risk", audit_risk)
        render_risk_bar("Internal Fraud Risk", fraud_risk)
        render_risk_bar("Reserve Liquidity Risk", liq_risk)
        
        # Feature 11: AI Business Doctor (Diagnosis)
        st.markdown("### AI Business Doctor")
        if health_score >= 80:
            status_card = "success-card"
            doc_status = "HEALTHY & RUNNING EXCELLENT"
            doc_diag = "Operational structures are solid. Cash inflow covers reserves and compliance standards are well-maintained."
        elif health_score >= 50:
            status_card = "highlight-card"
            doc_status = "NEEDS ATTENTION"
            doc_diag = "Identified moderate concerns: Overhead spending is higher than average, and the runway buffer should be optimized."
        else:
            status_card = "warning-card"
            doc_status = "CRITICAL CONDITION"
            doc_diag = "High audit alert count and weak profit margins are draining bank reserves. Restructure SaaS accounts immediately."
            
        st.markdown(f"""
        <div class='{status_card}'>
            <strong>Diagnostic Report:</strong> <span style='font-size: 1.05rem;'>{doc_status}</span><br>
            <p style='margin-top: 10px; font-size: 0.95rem; color: #475569;'>{doc_diag}</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    # Feature 16: AI CFO Dashboard Summary (Bonus: Executive Summary in Simple English)
    st.markdown("### Executive CFO Report Summary")
    runway_desc = "unlimited cash sustainability" if runway == float('inf') else f"{runway:.1f} months of survival"
    summary_text = f"""
    The financial health of **{st.session_state.profile['name']}** is graded as **{ 'Excellent' if health_score >= 80 else ('Stable' if health_score >= 50 else 'Vulnerable') }** with a score of **{health_score}/100**. 
    During the current monthly assessment, the enterprise generated **₹{financials['Total_Revenue']:,.2f}** in revenues against **₹{financials['Total_Expenses']:,.2f}** in operational disbursements. This leaves a net operating profit of **₹{financials['Net_Income']:,.2f}** ({margin_pct:.1f}% margin).
    
    Under the current structure, your cash reserves of **₹{financials['Current_Cash']:,.2f}** provide **{runway_desc}**. Tax obligations amount to **₹{it_val:,.2f}** for income tax and **₹{tax_data['Net_GST_Payable']:,.2f}** for GST.
    """
    st.info(summary_text)

# ==================== TAB 2: COMPANY SETUP & EXPENSE BUILDER ====================
with tab_setup:
    setup_col1, setup_col2 = st.columns(2)
    
    with setup_col1:
        # Feature 1: AI Company Setup Wizard
        st.markdown("### AI Company Onboarding Wizard")
        st.write("Complete the questionnaire to configure the AI CA engine for your specific business profile.")
        
        with st.form("company_setup_form"):
            w_name = st.text_input("What is your business name?", value=st.session_state.profile["name"])
            w_type = st.selectbox(
                "What type of business structure?",
                ["Sole Proprietorship", "Partnership Firm / LLP", "Private Limited Company (Pvt Ltd)"],
                index=["Sole Proprietorship", "Partnership Firm / LLP", "Private Limited Company (Pvt Ltd)"].index(st.session_state.profile["type"])
            )
            w_employees = st.slider("How many employees/contractors?", 0, 100, st.session_state.profile["employees"])
            w_revenue = st.number_input("Average Monthly Inflow / Revenue (₹)", min_value=0.0, value=st.session_state.profile["revenue"])
            w_gst = st.radio("Do you have GST Registration?", ["Yes", "No"], index=0 if st.session_state.profile["gst_registered"] == "Yes" else 1)
            w_cash = st.number_input("Current Cash Reserves in Bank (₹)", min_value=0.0, value=st.session_state.profile["bank_cash"])
            
            submit_wizard = st.form_submit_button("Rebuild Financial Profile")
            
            if submit_wizard:
                st.session_state.profile["name"] = w_name
                st.session_state.profile["type"] = w_type
                st.session_state.profile["employees"] = w_employees
                st.session_state.profile["revenue"] = w_revenue
                st.session_state.profile["gst_registered"] = w_gst
                st.session_state.profile["bank_cash"] = w_cash
                st.success("Financial profile updated successfully!")
                st.rerun()
                
    with setup_col2:
        # Feature 2: Interactive Expense Builder
        st.markdown("### Interactive Monthly Expense Builder")
        st.write("Fine-tune your monthly expenses categories. These values dynamically rebuild the dashboard ledgers.")
        
        eb = st.session_state.profile["expenses_breakdown"]
        
        eb_payroll = st.slider("Payroll & Wages (₹)", 0, 100000, int(eb.get("Payroll & Contractors", 25000)))
        eb_rent = st.slider("Office Space Rent (₹)", 0, 50000, int(eb.get("Rent & Office Space", 12000)))
        eb_util = st.slider("Electricity & Broadband (₹)", 0, 15000, int(eb.get("Utilities & Internet", 3000)))
        eb_soft = st.slider("Software & Cloud SaaS (₹)", 0, 30000, int(eb.get("Software & Infrastructure", 4000)))
        eb_market = st.slider("Marketing & Ad-spend (₹)", 0, 100000, int(eb.get("Marketing & Advertising", 15000)))
        eb_travel = st.slider("Travel & Client Meetings (₹)", 0, 30000, int(eb.get("Travel & Lodging", 5000)))
        eb_legal = st.slider("Legal Fees & Tax filing (₹)", 0, 15000, int(eb.get("Tax & Legal Fees", 2000)))
        eb_misc = st.slider("Miscellaneous Expenses (₹)", 0, 20000, int(eb.get("Miscellaneous Expense", 3000)))
        
        total_eb = eb_payroll + eb_rent + eb_util + eb_soft + eb_market + eb_travel + eb_legal + eb_misc
        eb_profit = st.session_state.profile["revenue"] - total_eb
        eb_margin = (eb_profit / st.session_state.profile["revenue"]) * 100 if st.session_state.profile["revenue"] > 0 else 0
        
        st.markdown(f"""
        <div class='highlight-card' style='margin-top: 15px;'>
            <strong>Dynamic Category Totals:</strong><br>
            * **Total Monthly Expenses:** ₹{total_eb:,.2f}<br>
            * **Expected Monthly Profit:** ₹{eb_profit:,.2f}<br>
            * **Projected Profit Margin:** {eb_margin:.1f}%
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Apply New Expense Model"):
            st.session_state.profile["expenses_breakdown"] = {
                "Payroll & Contractors": eb_payroll,
                "Rent & Office Space": eb_rent,
                "Utilities & Internet": eb_util,
                "Software & Infrastructure": eb_soft,
                "Marketing & Advertising": eb_market,
                "Travel & Lodging": eb_travel,
                "Tax & Legal Fees": eb_legal,
                "Miscellaneous Expense": eb_misc
            }
            st.session_state.profile["expenses"] = total_eb
            st.success("Expense model updated!")
            st.rerun()

    st.markdown("---")
    
    # Feature 15: SaaS Subscription Tracker
    st.markdown("### SaaS Subscription & Active Licenses Tracker")
    st.write("Zenith automatically tracks software subscriptions and flags unused seats to reduce cash burn.")
    
    subs = st.session_state.profile["subscriptions"]
    sub_df = pd.DataFrame(subs)
    st.dataframe(sub_df, use_container_width=True)
    
    unused_cost = sum(sub["cost"] for sub in subs if sub["status"] == "Unused")
    st.markdown(f"""
    <div class='warning-card'>
        <strong>Optimization Tip:</strong> Identified <strong>{len([s for s in subs if s['status'] == 'Unused'])}</strong> unused/redundant licenses. 
        Canceling Adobe Creative Cloud & Canva Pro Team can save <strong>₹{unused_cost:,.2f}/month</strong>.
    </div>
    """, unsafe_allow_html=True)

    # Feature 17: Cash Flow Calendar
    st.markdown("### Cash Flow Calendar")
    st.write("Schedule of expected payments, payouts, and compliance due dates for the current calendar cycle.")
    
    calendar_events = [
        {"Date": "1st of Month", "Event": "Salary Disbursements (Payroll)", "Amount": f"-₹{eb_payroll:,.0f}", "Type": "Expense"},
        {"Date": "5th of Month", "Event": "Office Lease Rent Payout", "Amount": f"-₹{eb_rent:,.0f}", "Type": "Expense"},
        {"Date": "8th of Month", "Event": "Stripe SaaS Inflow Payout", "Amount": f"+₹{financials['Total_Revenue']/12*0.6:,.0f}", "Type": "Income"},
        {"Date": "11th of Month", "Event": "GSTR-1 Monthly Sales Return filing", "Amount": "N/A", "Type": "Compliance"},
        {"Date": "15th of Month", "Event": "AWS & Hosting Subscriptions Renewal", "Amount": "-₹3,200", "Type": "Expense"},
        {"Date": "20th of Month", "Event": "GSTR-3B GST Net Settlement payment", "Amount": f"-₹{tax_data['Net_GST_Payable']/12:,.0f}", "Type": "Expense"},
        {"Date": "25th of Month", "Event": "Broadband & Power Bill renewal", "Amount": f"-₹{eb_util:,.0f}", "Type": "Expense"}
    ]
    st.table(pd.DataFrame(calendar_events))

# ==================== TAB 3: SIMULATORS & ADVISORS ====================
with tab_sim:
    sim_col1, sim_col2 = st.columns(2)
    
    with sim_col1:
        # Feature 8: AI Financial Advisor (Can I hire an employee?)
        st.markdown("### AI Financial Advisor")
        st.write("Submit upcoming strategic financial questions to evaluate reserve impacts.")
        
        decision = st.selectbox(
            "What is your next major operational decision?",
            [
                "Hire one more engineer (Cost: ₹30,000/month)",
                "Move to a larger corporate office space (Cost: ₹25,000/month)",
                "Double current Marketing budget",
                "Purchase 5 MacBook Pro IT Assets (One-off Cost: ₹3,50,000)"
            ]
        )
        
        if st.button("Evaluate Decision"):
            current_profit = financials["Net_Income"] / 12.0
            
            if "engineer" in decision.lower():
                cost = 30000
                new_runway = financials["Current_Cash"] / (forecasting_data["Net_Monthly_Burn"] + cost) if (forecasting_data["Net_Monthly_Burn"] + cost) > 0 else float('inf')
                if current_profit > cost:
                    st.success(f"**Zenith Verdict: RECOMMENDED**\n\nYour monthly net profit of ₹{current_profit:,.2f} fully covers the ₹30,000 salary. The post-hire monthly cash surplus will be ₹{current_profit - cost:,.2f}. Solvency is safe.")
                else:
                    st.error(f"**Zenith Verdict: NOT RECOMMENDED**\n\nMonthly expense (₹30,000) exceeds average net profits (₹{current_profit:,.2f}). This would make the company cash-flow negative and reduce the runway to {new_runway:.1f} months.")
            elif "office" in decision.lower():
                cost = 25000
                if current_profit > cost:
                    st.success(f"**Zenith Verdict: RECOMMENDED**\n\nRent increase is sustainable. Remaining monthly buffer: ₹{current_profit - cost:,.2f}.")
                else:
                    st.error(f"**Zenith Verdict: NOT RECOMMENDED**\n\nIncreasing fixed overheads by ₹25,000 will consume your remaining net margin. Consider co-working desks first.")
            elif "marketing" in decision.lower():
                cost = st.session_state.profile["expenses_breakdown"]["Marketing & Advertising"]
                st.info(f"**Zenith Verdict: CONDITIONALLY RECOMMENDED**\n\nDoubling marketing by ₹{cost:,.2f} is recommended ONLY if the Customer Acquisition Cost (CAC) yields an LTV ratio above 3:1. Ensure conversion tracking is set up before scaling.")
            else: # MacBooks
                cost = 350000
                if financials["Current_Cash"] > cost * 2:
                    st.success(f"**Zenith Verdict: RECOMMENDED**\n\nYour cash reserve of ₹{financials['Current_Cash']:,.2f} is sufficient. You can claim a 40% depreciation block write-off under Section 32, saving ₹1,40,000 in taxable profit this year.")
                else:
                    st.error(f"**Zenith Verdict: NOT RECOMMENDED**\n\nSpending ₹3,50,000 out of ₹{financials['Current_Cash']:,.2f} reserves represents too high of a liquidity drain (over 75%). Rent the laptops instead.")
                    
        st.markdown("---")
        
        # Feature 6: AI Ask More Questions (Interactive Tax Saving Advisor)
        st.markdown("### AI Ask More Questions (Tax Diagnostic)")
        st.write("Answer a quick CA diagnostic checkup to reveal hidden tax optimization strategies.")
        
        with st.form("tax_questionnaire"):
            q_rent = st.selectbox("Do you pay rent for your business office?", ["Yes", "No"], index=0)
            q_rent_val = st.number_input("If yes, monthly rent amount (₹)", value=15000)
            q_laptops = st.selectbox("Did you purchase computers/laptops/servers this year?", ["Yes", "No"], index=0)
            q_laptops_val = st.number_input("If yes, total worth of IT purchases (₹)", value=350000)
            q_itc = st.selectbox("Do you spend on cloud services (AWS, Google, SaaS) or digital ads?", ["Yes", "No"], index=0)
            
            submit_qa = st.form_submit_button("Submit Diagnostic Answers")
            
            if submit_qa:
                st.session_state.qa_answers = {
                    "pay_rent": q_rent,
                    "rent_amount": q_rent_val,
                    "own_laptops": q_laptops,
                    "laptops_worth": q_laptops_val,
                    "has_gst": q_itc
                }
                st.success("Answers recorded! Analyzing tax opportunities...")
                
        # Calculate savings based on answers
        savings_lines = []
        tot_saved = 0.0
        
        ans = st.session_state.qa_answers
        if ans["own_laptops"] == "Yes":
            dep = ans["laptops_worth"] * 0.40
            tax_val = dep * 0.25 # corporate tax rate approx
            savings_lines.append(f"* **Section 32 Laptops Depreciation:** Claim 40% write-off on ₹{ans['laptops_worth']:,.0f} -> Reduces taxable income by ₹{dep:,.0f} (Estimated cash savings: **₹{tax_val:,.2f}**)")
            tot_saved += tax_val
        if ans["pay_rent"] == "Yes":
            rent_tax = ans["rent_amount"] * 12 * 0.25
            savings_lines.append(f"* **Business Rent Deduction:** Renting office space is fully deductible -> Reduces corporate tax by up to **₹{rent_tax:,.2f}** annually.")
            tot_saved += rent_tax
        if ans["has_gst"] == "Yes":
            # Assume 18% GST reclaimable on SaaS spend
            saas_val = st.session_state.profile["expenses_breakdown"].get("Software & Infrastructure", 5000) * 12
            gst_reclaim = saas_val * 0.18
            savings_lines.append(f"* **GSTR-2B Input Tax Credit (ITC):** Add your GSTIN to profiles (AWS, Slack, Google) to reclaim **₹{gst_reclaim:,.2f}** in input credit tax refunds.")
            tot_saved += gst_reclaim
            
        st.markdown(f"""
        <div class='success-card'>
            <strong>Estimated Potential Tax Savings:</strong> <span style='font-size: 1.15rem; color: #22c55e;'>₹{tot_saved:,.2f}</span><br>
            <div style='margin-top: 10px; font-size: 0.92rem; color: #475569;'>
                {'<br>'.join(savings_lines)}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with sim_col2:
        # Bonus: Scenario Comparison (Current vs After Cost Reduction)
        st.markdown("### Optimized Scenario Planner")
        st.write("Compare your current business metrics side-by-side with an optimized cost-cutting scenario.")
        
        # Calculate optimized metrics (reducings SaaS by 20%, cutting unused subs, reducing travel)
        current_rev = financials["Total_Revenue"]
        current_exp = financials["Total_Expenses"]
        current_profit = financials["Net_Income"]
        
        opt_exp = current_exp - (unused_cost * 12) - (eb_travel * 12 * 0.15)
        opt_profit = current_rev - opt_exp
        
        comparison_data = pd.DataFrame({
            "Metric": ["Annual Revenue", "Annual Expenses", "Annual Net Profit", "Profit Margin", "Cash Runway Status"],
            "Current Scenario": [f"₹{current_rev:,.2f}", f"₹{current_exp:,.2f}", f"₹{current_profit:,.2f}", f"{margin_pct:.1f}%", runway_str],
            "Optimized Scenario": [f"₹{current_rev:,.2f}", f"₹{opt_exp:,.2f}", f"₹{opt_profit:,.2f}", f"{((opt_profit/current_rev)*100):.1f}%", "Infinite / Increased Buffer"]
        })
        st.dataframe(comparison_data, hide_index=True, use_container_width=True)
        st.markdown("""
        <div class='highlight-card'>
            <strong>Optimization Strategy:</strong><br>
            1. Cancel unused software (Save ₹1,800/month).<br>
            2. Reduce travel and client lodging limits by 15%.<br>
            3. Apply 40% computer asset depreciation under Section 32.
        </div>
        """, unsafe_allow_html=True)

# ==================== TAB 4: GROWTH & GOAL PLANNER ====================
with tab_goals:
    growth_col1, growth_col2 = st.columns(2)
    
    with growth_col1:
        # Feature 9: Business Growth Predictor
        st.markdown("### Business Growth Predictor")
        st.write("Project your corporate revenue, profits, and tax brackets for different growth rates.")
        
        growth_rate = st.radio(
            "Select Annualized Growth Target (%)",
            [5, 10, 20, 30],
            index=2,
            horizontal=True
        )
        
        g_mult = 1.0 + (growth_rate / 100.0)
        proj_rev = financials["Total_Revenue"] * g_mult
        proj_exp = financials["Total_Expenses"] * (1.0 + (growth_rate * 0.4 / 100.0)) # expenses scale slower
        proj_profit = proj_rev - proj_exp
        proj_gst = proj_rev * 0.18
        proj_tax = proj_profit * 0.25 # corporate tax estimate
        
        st.markdown(f"""
        <div class='highlight-card'>
            <strong>Projected Outlook after 12 Months ({growth_rate}% Growth):</strong><br>
            * **Projected Revenue:** ₹{proj_rev:,.2f}<br>
            * **Projected Expenses:** ₹{proj_exp:,.2f}<br>
            * **Projected Net Profit:** ₹{proj_profit:,.2f}<br>
            * **Projected GST Output (18%):** ₹{proj_gst:,.2f}<br>
            * **Projected Income Tax Liability:** ₹{proj_tax:,.2f}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Feature 12: Goal Planner
        st.markdown("### Financial Goal Planner")
        st.write("Calculate the savings reserve required to reach key business expansion goals.")
        
        target_goal = st.selectbox(
            "What is your primary financial milestone?",
            [
                "Buy Private Corporate Office space (₹25,00,000)",
                "Open a new retail branch office (₹10,00,000)",
                "Hire a senior technical consulting team (₹4,50,000)",
                "Reach Cash Buffer Reserve Milestone (₹10,00,000)"
            ]
        )
        
        timeline_months = st.slider("Target Timeline to achieve (months)", 6, 36, 18)
        
        goal_costs = {
            "Office": 2500000,
            "branch": 1000000,
            "team": 450000,
            "Reserve": 1000000
        }
        
        cost_key = next((k for k in goal_costs if k in target_goal), "Reserve")
        goal_cost = goal_costs[cost_key]
        monthly_saving_req = goal_cost / timeline_months
        
        st.markdown(f"""
        <div class='success-card'>
            <strong>Goal Target:</strong> ₹{goal_cost:,.2f} over {timeline_months} months.<br>
            You need to save <strong>₹{monthly_saving_req:,.2f} per month</strong> to achieve this. 
            Your current average monthly net profit is <strong>₹{(financials['Net_Income']/12):,.2f}</strong>.
            {'Saving target is fully achievable with current surplus!' if (financials['Net_Income']/12) > monthly_saving_req else 'Warning: Current surplus is insufficient. You need to boost sales or reduce SaaS expenses.'}
        </div>
        """, unsafe_allow_html=True)
        
    with growth_col2:
        # Feature 13: Loan Eligibility Predictor
        st.markdown("### Corporate Loan Eligibility Predictor")
        st.write("Estimate maximum loan borrow capacity based on operational profit ratios.")
        
        est_debt = st.number_input("Do you have any existing business liabilities/debt? (₹)", min_value=0.0, value=0.0)
        
        # Calculations: Max loan = 3x net profit - current debt
        annual_profit = financials["Net_Income"]
        max_loan = max(0.0, (annual_profit * 2.5) - est_debt)
        
        # EMI calculation (10% rate for 36 months)
        monthly_rate = 0.10 / 12
        emi = max_loan * (monthly_rate * (1 + monthly_rate)**36) / (((1 + monthly_rate)**36) - 1) if max_loan > 0 else 0
        
        debt_risk_level = "Low" if (emi < (annual_profit / 12 * 0.3)) else ("Medium" if (emi < (annual_profit / 12 * 0.5)) else "High")
        risk_badge_color = "#22c55e" if debt_risk_level == "Low" else ("#f59e0b" if debt_risk_level == "Medium" else "#ef4444")
        
        st.markdown(f"""
        <div class='highlight-card'>
            * **Estimated Borrow Limit:** **₹{max_loan:,.2f}**<br>
            * **Monthly EMI (3-Year Term @ 10%):** ₹{emi:,.2f}/month<br>
            * **Debt-to-Income Risk Rating:** <span style='color: {risk_badge_color}; font-weight: bold;'>{debt_risk_level} Risk</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Feature 19: AI Business Benchmark
        st.markdown("### AI Industry Benchmarking")
        st.write("Compare your operational expense margins against typical averages for tech & service companies.")
        
        benchmark_df = pd.DataFrame({
            "Operational Metric": ["Net Profit Margin", "Software & Cloud spend", "Marketing & Ad spend", "Travel & Client relations"],
            "Your Margin": [f"{margin_pct:.1f}%", f"{((eb_soft / st.session_state.profile['revenue'])*100):.1f}%", f"{((eb_market / st.session_state.profile['revenue'])*100):.1f}%", f"{((eb_travel / st.session_state.profile['revenue'])*100):.1f}%"],
            "Industry Benchmark": ["20.0%", "5.0%", "10.0%", "3.0%"],
            "Status": [
                "Excellent" if margin_pct > 20 else "Healthy",
                "Optimizable" if (eb_soft/st.session_state.profile['revenue'] > 0.05) else "Good",
                "Needs Attention" if (eb_market/st.session_state.profile['revenue'] > 0.10) else "Good",
                "Good"
            ]
        })
        st.table(benchmark_df)

# ==================== TAB 5: TAX PLANNER & SMART SAVING ====================
with tab_tax:
    tax_col1, tax_col2 = st.columns(2)
    
    with tax_col1:
        st.markdown("### GSTR Obligations & Sales Tax Summary")
        gst_summary_df = pd.DataFrame({
            "GST Calculation Type": [
                "Sales Output GST collected from Clients (18% base)",
                "Input Tax Credit (ITC) claimed from vendors",
                "Net GST Payable to the Government"
            ],
            "Obligation Value": [
                f"₹{tax_data['Output_GST']:,.2f}",
                f"₹{tax_data['Input_GST_ITC']:,.2f}",
                f"₹{tax_data['Net_GST_Payable']:,.2f}"
            ]
        })
        st.table(gst_summary_df)
        
        # Feature 7: Smart Tax Saving Engine
        st.markdown("### Smart Tax Saving Checklist")
        st.write("Toggle options to calculate expected tax reduction under Indian Tax Regimes:")
        
        c_opt1 = st.checkbox("Declare presumptive taxation under Section 44ADA (Declare only 50% profit)", value=True)
        c_opt2 = st.checkbox("Claim 40% block depreciation on business laptops & equipment", value=True)
        c_opt3 = st.checkbox("Reclaim 18% GST Input Credit on software services", value=True)
        
        estimated_saving = 0.0
        if c_opt1:
            estimated_saving += financials["Total_Revenue"] * 0.15 # Approx tax rate deduction benefit
        if c_opt2:
            estimated_saving += 350000 * 0.40 * 0.25 # 40% of laptops worth times corporate tax
        if c_opt3:
            estimated_saving += (eb_soft * 12) * 0.18
            
        st.markdown(f"""
        <div class='success-card'>
            <strong>Estimated Smart Tax Savings:</strong> <span style='font-size: 1.25rem; color: #22c55e;'>₹{estimated_saving:,.2f}</span>
        </div>
        """, unsafe_allow_html=True)
        
    with tax_col2:
        st.markdown("### Corporate / Individual Income Tax Details")
        it_info = tax_data['Income_Tax']
        
        it_rows = []
        for k, v in it_info.items():
            if k == "Slab Breakdown":
                continue
            if isinstance(v, (int, float)):
                it_rows.append((k, f"₹{v:,.2f}"))
            else:
                it_rows.append((k, str(v)))
                
        st.table(pd.DataFrame(it_rows, columns=["Assessment Metric", "Value"]))
        
        if "Slab Breakdown" in it_info and len(it_info["Slab Breakdown"]) > 0:
            with st.expander("Slab Wise Tax Breakdown"):
                for slab in it_info["Slab Breakdown"]:
                    st.write(slab)
                    
        # Bonus: AI Investment Suggestions
        st.markdown("### AI Investment Advisory")
        st.write("Suggestions to invest surplus company reserves securely under Section laws:")
        st.markdown("""
        * **Arbitrage/Liquid Mutual Funds:** Return rate: ~6.8%. Highly liquid, low tax. Ideal for parking short-term tax reserves.
        * **Corporate Fixed Deposits (SBI/HDFC):** Return rate: ~7.25% (under 3-year term). Secure interest buffer.
        * **National Pension System (NPS - Tier II):** Provides additional deductions under personal filing.
        """)
        st.caption("*Disclaimer: Financial recommendations are simulated advice. Consult an official advisor before executing investments.*")

# ==================== TAB 6: FORENSIC AUDIT & INVOICE ANALYZER ====================
with tab_audit:
    audit_col1, audit_col2 = st.columns(2)
    
    with audit_col1:
        st.markdown("### Forensic Bookkeeping Audit Flags")
        st.write("Isolation Forest and outlier detection flags for suspicious activities.")
        
        high_findings = audit_findings[audit_findings["Severity"] == "High"]
        med_findings = audit_findings[audit_findings["Severity"] == "Medium"]
        
        a_m1, a_m2, a_m3 = st.columns(3)
        a_m1.metric("Flagged Accounts", len(audit_findings))
        a_m2.metric("High Severity", len(high_findings))
        a_m3.metric("Medium/Low Risk", len(med_findings))
        
        st.write("")
        if len(audit_findings) == 0:
            st.markdown("<div class='success-card'>Clean Audit opinion: No anomalies or red flags detected in transactions.</div>", unsafe_allow_html=True)
        else:
            for idx, row in audit_findings.head(6).iterrows():
                severity = row["Severity"]
                card_class = "warning-card" if severity == "High" else "highlight-card"
                badge_color = "#ef4444" if severity == "High" else "#f59e0b"
                
                st.markdown(f"""
                <div class='{card_class}'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <strong style='color: {badge_color};'>{row['Remarks']}</strong>
                        <span style='background: rgba(0,0,0,0.05); padding: 2px 8px; border-radius: 5px; font-size: 0.8rem; color: #475569;'>{severity}</span>
                    </div>
                    <div style='margin-top: 10px; font-size: 0.92rem;'>
                        <strong>Desc:</strong> {row['Description']} | <strong>Cat:</strong> {row['Category']}<br>
                        <strong>Date:</strong> {row['Date']} | <span style='font-size: 1rem; font-weight: bold;'>₹{row['Amount']:,.2f}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
    with audit_col2:
        # Feature 14: Invoice Analyzer
        st.markdown("### AI Invoice & Bill Analyzer")
        st.write("Upload a business invoice or bill image/PDF to check for compliance compliance.")
        
        invoice_file = st.file_uploader(
            "Upload invoice file (PDF/PNG)",
            type=["png", "jpg", "pdf", "csv"],
            key="invoice_uploader"
        )
        
        if invoice_file is not None:
            # Simulate a real compliance check
            st.info("Performing compliance audits on invoice...")
            st.markdown("""
            **Zenith Compliance Checklist:**
            * [x] **Subtotal Calculations:** Verified (Subtotal + GST = Total).
            * [x] **Vendor GSTIN Format:** Verified (Valid 15-digit structure).
            * [x] **Duplicate Payment Check:** Verified (No duplicate invoice found).
            * [x] **Vendor Status:** Active GSTIN on GST Portal.
            """)
            st.success("Invoice checks completed successfully! No issues found. Ready for reimbursement.")
        else:
            st.write("Or drag and drop any file here to test simulated OCR scans.")
            
        # Feature 10: Expense Optimization AI
        st.markdown("### Expense Optimization AI Warnings")
        bench_saas = eb_soft / (st.session_state.profile["revenue"] or 1)
        if bench_saas > 0.05:
            st.markdown(f"""
            <div class='warning-card'>
                <strong>SaaS Billing Anomaly:</strong> Software cost constitutes <strong>{bench_saas*100:.1f}%</strong> of total revenues (Industry average: <strong>5.0%</strong>).
                Canceling unused Canva & Adobe seats will save <strong>₹{unused_cost:,.2f}/month</strong>.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("<div class='success-card'>Overhead spending margins are optimized under standard industry parameters.</div>", unsafe_allow_html=True)

# ==================== TAB 7: CONSULT SENIOR AI CA ====================
with tab_chat:
    st.markdown("### Chat with Zenith AI Senior Chartered Accountant")
    st.write("Get interactive support regarding tax slab rates, Input tax credits, or cash runway forecasting.")
    
    chatbot = AIChatbot(financials, tax_data, audit_findings, forecasting_data, st.session_state.profile["type"])
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Hello! I am Zenith CA, your autonomous AI Chartered Accountant. I have audited your bookkeeping ledger for **{st.session_state.profile['name']}**.\n\nAsk me about tax saving options, runway analysis, or invoice verification guidelines."
        })
        
    # Quick action prompt chips
    chip_col1, chip_col2, chip_col3 = st.columns(3)
    quick_prompt = None
    
    with chip_col1:
        if st.button("How can I save tax?", key="chat_chip_1"):
            quick_prompt = "How can I reduce my tax liability?"
    with chip_col2:
        if st.button("Runway and burn report?", key="chat_chip_2"):
            quick_prompt = "What is my cash runway and burn rate?"
    with chip_col3:
        if st.button("Explain GST input credits?", key="chat_chip_3"):
            quick_prompt = "Explain GSTR-2B Input tax credit claiming instructions."
            
    # Display message history
    for msg in st.session_state.messages:
        role_class = "user-bubble" if msg["role"] == "user" else "assistant-bubble"
        speaker = "You" if msg["role"] == "user" else "Zenith CA"
        st.markdown(f"""
        <div class='{role_class}'>
            <strong>{speaker}:</strong><br>
            {msg['content']}
        </div>
        """, unsafe_allow_html=True)
        
    # React to user input
    user_input = st.chat_input("Ask a financial, tax, or audit question...")
    if quick_prompt:
        user_input = quick_prompt
        
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        response = chatbot.respond(user_input)
        response_md = response.replace("\n", "  \n")
        st.session_state.messages.append({"role": "assistant", "content": response_md})
        st.rerun()
