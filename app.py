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

# Custom CSS for Light Theme & White Aesthetics
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    /* Apply Font */
    html, body, [class*="css"], .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Main Background - Slate/Blue Gradient on Light Background */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #eff6ff 100%) !important;
        color: #0f172a !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    
    /* Clean White Metrics Cards */
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
        transform: translateY(-5px) !important;
        border-color: #2563eb !important;
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.1), 0 4px 6px -2px rgba(37, 99, 235, 0.05) !important;
    }
    
    /* Metrics fonts */
    div[data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
    }
    
    div[data-testid="stMetricValue"] {
        color: #0f172a !important;
    }
    
    /* Custom headers */
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
    
    /* Tabs customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #e2e8f0 !important;
        padding: 8px !important;
        border-radius: 10px !important;
        border: 1px solid #cbd5e1 !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px !important;
        white-space: pre-wrap !important;
        background-color: transparent !important;
        border-radius: 8px !important;
        color: #475569 !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 0px 20px !important;
        transition: all 0.2s ease !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #0f172a !important;
        background-color: rgba(0, 0, 0, 0.04) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2563eb !important;
        color: #ffffff !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.2) !important;
    }
    
    /* Highlight Cards */
    .highlight-card {
        background: #ffffff;
        border: 1px solid #bfdbfe;
        border-left: 5px solid #2563eb;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
    }
    
    .warning-card {
        background: #ffffff;
        border: 1px solid #fecaca;
        border-left: 5px solid #ef4444;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
    }
    
    .success-card {
        background: #ffffff;
        border: 1px solid #bbf7d0;
        border-left: 5px solid #22c55e;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
    }
    
    /* Buttons */
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
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
    }
    
    /* Chat bubbles */
    .user-bubble {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 15px 15px 0px 15px;
        padding: 15px;
        margin: 10px 0px;
        text-align: right;
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

# Main Title & Subtitle (No emoji)
st.markdown("<h1 class='main-title'>Zenith CA</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Autonomous AI-Powered Chartered Accountant, Auditor and Tax Advisor</p>", unsafe_allow_html=True)

# --- SIDEBAR: Settings & File Upload ---
st.sidebar.markdown("### Entity Profile")
business_type = st.sidebar.selectbox(
    "Business Structure",
    ["Sole Proprietorship", "Partnership Firm / LLP", "Private Limited Company (Pvt Ltd)"],
    index=2
)

salary_drawn = st.sidebar.number_input(
    "Salary Drawn by Owner/Directors (Annual - ₹)",
    min_value=0.0,
    value=1200000.0,
    step=50000.0,
    help="Salaries are treated as business expenses and are tax-deductible for corporate income tax."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Financial Data Input")
uploaded_file = st.sidebar.file_uploader(
    "Upload Transaction Ledger (CSV)",
    type=["csv"],
    help="Upload your bank statement or general ledger. Expected columns: Date, Description, Amount, Type (Income/Expense)"
)

# Helper function to load and parse the uploaded file or generate demo data
@st.cache_data
def load_transaction_data(file_obj=None):
    if file_obj is not None:
        try:
            df = pd.read_csv(file_obj)
            
            # Map column names automatically
            col_mapping = {}
            for col in df.columns:
                col_lower = col.lower()
                if "date" in col_lower or "timestamp" in col_lower:
                    col_mapping[col] = "Date"
                elif "desc" in col_lower or "particular" in col_lower or "narrative" in col_lower:
                    col_mapping[col] = "Description"
                elif "amount" in col_lower or "value" in col_lower or "dr" in col_lower or "cr" in col_lower:
                    col_mapping[col] = "Amount"
                elif "type" in col_lower or "category" in col_lower or "flow" in col_lower:
                    col_mapping[col] = "Type"
                    
            df = df.rename(columns=col_mapping)
            
            # Check for core columns
            required_cols = ["Date", "Description", "Amount"]
            for col in required_cols:
                if col not in df.columns:
                    st.error(f"Missing required column in CSV: '{col}'. Please check your CSV format.")
                    return generate_mock_transactions()
            
            # Parse Date
            df["Date"] = pd.to_datetime(df["Date"]).dt.date
            # Clean Amount
            df["Amount"] = pd.to_numeric(df["Amount"].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0.0)
            
            # Handle 'Type' if missing
            if "Type" not in df.columns:
                if (df["Amount"] < 0).any():
                    df["Type"] = df["Amount"].apply(lambda x: "Expense" if x < 0 else "Income")
                    df["Amount"] = df["Amount"].abs()
                else:
                    df["Type"] = "Expense"
            else:
                df["Type"] = df["Type"].apply(lambda x: "Income" if "inc" in str(x).lower() or "cr" in str(x).lower() or "in" in str(x).lower() else "Expense")
                
            # Populate Transaction_ID
            df["Transaction_ID"] = [f"TX-{1000 + i}" for i in range(len(df))]
            
            # Categorize descriptions using ML model
            clf = TransactionClassifier()
            df["Category"] = clf.predict(df["Description"].tolist())
            
            # Corrections
            df.loc[df["Type"] == "Income", "Category"] = "Revenue"
            df.loc[df["Description"].str.contains("rent|lease", case=False), "Category"] = "Rent & Office Space"
            df.loc[df["Description"].str.contains("payroll|salary|wages", case=False), "Category"] = "Payroll & Contractors"
            
            return df
            
        except Exception as e:
            st.error(f"Error parsing CSV: {e}. Falling back to default Demo ledger.")
            return generate_mock_transactions()
    else:
        return generate_mock_transactions()

# Load Data
df_transactions = load_transaction_data(uploaded_file)

# Run accounting equations
financials = calculate_financials(df_transactions)
tax_data = calculate_taxes(df_transactions, business_type, salary_drawn)
audit_findings = audit_transactions(df_transactions)
forecasting_data = forecast_financials(df_transactions)

# --- TOP METRICS PANEL ---
m_col1, m_col2, m_col3, m_col4, m_col5, m_col6 = st.columns(6)

with m_col1:
    st.metric(
        label="Total Revenue",
        value=f"₹{financials['Total_Revenue']:,.0f}",
        delta=None
    )
with m_col2:
    st.metric(
        label="Total Expenses",
        value=f"₹{financials['Total_Expenses']:,.0f}",
        delta=None
    )
with m_col3:
    net_val = financials['Net_Income']
    st.metric(
        label="Net Operating Income",
        value=f"₹{net_val:,.0f}",
        delta=f"{((net_val/financials['Total_Revenue'])*100 if financials['Total_Revenue'] > 0 else 0):.1f}% Margin",
        delta_color="normal" if net_val > 0 else "inverse"
    )
with m_col4:
    gst_val = tax_data['Net_GST_Payable']
    st.metric(
        label="Est. Net GST Due",
        value=f"₹{gst_val:,.0f}",
        delta="Input credit deducted",
        delta_color="off"
    )
with m_col5:
    it_info = tax_data['Income_Tax']
    it_val = it_info.get("Total Income Tax Payable", it_info.get("Total_Income_Tax Payable", 0))
    st.metric(
        label="Income Tax Payable",
        value=f"₹{it_val:,.0f}",
        delta=f"Effective: {it_info.get('Effective Tax Rate', 'N/A')}",
        delta_color="off"
    )
with m_col6:
    runway = forecasting_data['Runway_Months']
    runway_str = f"{runway:.1f} Mon" if runway != float('inf') else "Positive"
    st.metric(
        label="Cash Runway",
        value=runway_str,
        delta=f"Cash: ₹{financials['Current_Cash']:,.0f}",
        delta_color="normal" if runway == float('inf') or runway > 6 else "inverse"
    )

st.write("")

# --- PDF Generation Button in Sidebar (No emoji) ---
st.sidebar.markdown("### Export Official Report")
if st.sidebar.button("Generate Financial PDF"):
    try:
        pdf_bytes = generate_financial_pdf(financials, tax_data, audit_findings, business_type)
        st.sidebar.download_button(
            label="Download PDF Report",
            data=pdf_bytes,
            file_name=f"Zenith_CA_Financial_Report_{datetime.date.today().strftime('%Y_%m_%d')}.pdf",
            mime="application/pdf"
        )
        st.sidebar.success("PDF generated successfully! Click 'Download PDF Report' above.")
    except Exception as e:
        st.sidebar.error(f"Error compiling PDF: {e}")

# --- MAIN TABS LAYOUT (No emojis) ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Financial Control Center",
    "AI Forensic Audit",
    "Predictive Analytics & Runway",
    "Tax Planner & Optimizer",
    "Chat with AI Senior CA"
])

# ==================== TAB 1: FINANCIAL CONTROL CENTER ====================
with tab1:
    st.markdown("### Income & Balance Control Center")
    st.write("Complete bookkeeping ledgers processed with AI categorical distribution.")
    
    col_t1_1, col_t1_2 = st.columns(2)
    
    with col_t1_1:
        # Create double bar chart for Revenue vs Expenses month-over-month (Bars Blue)
        history = forecasting_data["Monthly_History"]
        history["Month_Str"] = history["YearMonth"].apply(lambda x: x.strftime("%b %y"))
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=history["Month_Str"],
            y=history["Income"],
            name="Revenue (Inflow)",
            marker_color="#1d4ed8",  # Royal Blue
            opacity=0.9
        ))
        fig.add_trace(go.Bar(
            x=history["Month_Str"],
            y=history["Expense"],
            name="Expenses (Outflow)",
            marker_color="#93c5fd",  # Sky Blue
            opacity=0.9
        ))
        fig.update_layout(
            title="Monthly Cash Inflow vs Outflow",
            barmode="group",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#0f172a",  # Dark text
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(15,23,42,0.06)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col_t1_2:
        # Expense Category breakdown pie chart (Shades of blue)
        cat_df = financials["Category_Breakdown"]
        cat_df = cat_df[cat_df["Category"] != "Revenue"]
        
        fig_pie = px.pie(
            cat_df,
            values="Amount",
            names="Category",
            hole=0.4,
            title="Operational Expense Allocation",
            color_discrete_sequence=px.colors.sequential.Blues_r  # Shades of blue
        )
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#0f172a",
            legend=dict(orientation="v", yanchor="middle", y=0.5)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    st.write("")
    
    # Balance Sheet Expansion (No emojis)
    st.markdown("### Simplified Projected Balance Sheet")
    bs_col1, bs_col2, bs_col3 = st.columns(3)
    
    bs = financials["Balance_Sheet"]
    
    with bs_col1:
        st.markdown("<div class='highlight-card'>", unsafe_allow_html=True)
        st.markdown("#### ASSETS")
        for asset, val in bs["Assets"].items():
            if asset == "Total Assets":
                st.markdown(f"**{asset}**: **₹{val:,.2f}**")
            else:
                st.markdown(f"* {asset}: ₹{val:,.2f}")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with bs_col2:
        st.markdown("<div class='highlight-card'>", unsafe_allow_html=True)
        st.markdown("#### LIABILITIES")
        for liab, val in bs["Liabilities"].items():
            if liab == "Total Liabilities":
                st.markdown(f"**{liab}**: **₹{val:,.2f}**")
            else:
                st.markdown(f"* {liab}: ₹{val:,.2f}")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with bs_col3:
        st.markdown("<div class='highlight-card'>", unsafe_allow_html=True)
        st.markdown("#### OWNER EQUITY")
        for eq, val in bs["Equity"].items():
            if eq == "Total Equity":
                st.markdown(f"**{eq}**: **₹{val:,.2f}**")
            else:
                st.markdown(f"* {eq}: ₹{val:,.2f}")
        st.markdown("</div>", unsafe_allow_html=True)

    # General Ledger Explorer
    st.write("")
    with st.expander("View General Ledger (Categorized Transactions)"):
        df_display = df_transactions.copy()
        df_display["Amount"] = df_display["Amount"].map(lambda x: f"₹{x:,.2f}")
        st.dataframe(
            df_display[["Transaction_ID", "Date", "Description", "Type", "Category", "Amount"]],
            use_container_width=True
        )

# ==================== TAB 2: AI FORENSIC AUDIT ====================
with tab2:
    st.markdown("### Forensic Transaction Auditing & Fraud Guard")
    st.write("Isolation Forest Anomaly detection and statistical ledger filters mapping audit risks.")
    
    # Summary of findings
    high_findings = audit_findings[audit_findings["Severity"] == "High"]
    med_findings = audit_findings[audit_findings["Severity"] == "Medium"]
    
    col_t2_1, col_t2_2, col_t2_3 = st.columns(3)
    with col_t2_1:
        st.metric("Total Flagged Transactions", len(audit_findings))
    with col_t2_2:
        st.metric("High Severity Risk", len(high_findings), delta_color="inverse")
    with col_t2_3:
        st.metric("Medium/Low Severity", len(med_findings))
        
    st.write("")
    
    if len(audit_findings) == 0:
        st.markdown("<div class='success-card'>Clean Audit opinion: No anomalies, duplicate invoicing, or suspicious transaction descriptions detected.</div>", unsafe_allow_html=True)
    else:
        st.markdown("#### Audit Red Flags & Warnings Log")
        
        # Display each anomaly with custom HTML card depending on severity (No emojis)
        for idx, row in audit_findings.iterrows():
            severity = row["Severity"]
            card_class = "warning-card" if severity == "High" else "highlight-card"
            badge_color = "#ef4444" if severity == "High" else "#f59e0b"
            
            st.markdown(f"""
            <div class='{card_class}'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <strong style='color: {badge_color};'>{row['Remarks']}</strong>
                    <span style='background: rgba(0,0,0,0.05); padding: 2px 8px; border-radius: 5px; font-size: 0.8rem; color: #475569;'>{severity} Severity</span>
                </div>
                <div style='margin-top: 10px; font-size: 0.95rem; color: #334155;'>
                    <strong>Description:</strong> {row['Description']} | <strong>Category:</strong> {row['Category']}
                </div>
                <div style='margin-top: 5px; font-size: 0.95rem; color: #64748b; display: flex; justify-content: space-between;'>
                    <span><strong>Date:</strong> {row['Date']}</span>
                    <span style='font-size: 1.1rem; color: #0f172a;'><strong>₹{row['Amount']:,.2f}</strong></span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==================== TAB 3: PREDICTIVE FORECASTING ====================
with tab3:
    st.markdown("### ML Cash Flow & Solvency Projections")
    st.write("Predictive time-series modeling projecting revenue, burn rate, and capital runway.")
    
    # Runway explanation
    col_t3_left, col_t3_right = st.columns([1, 2])
    
    with col_t3_left:
        st.markdown("#### Runway Health Dashboard")
        st.write(f"**Average Monthly Outflow (Burn):** ₹{forecasting_data['Avg_Monthly_Expenses']:,.2f}")
        st.write(f"**Average Monthly Inflow:** ₹{forecasting_data['Avg_Monthly_Income']:,.2f}")
        st.write(f"**Net Monthly Cash Flow:** ₹{forecasting_data['Avg_Monthly_Income'] - forecasting_data['Avg_Monthly_Expenses']:,.2f}")
        
        runway_val = forecasting_data['Runway_Months']
        if runway_val == float('inf'):
            st.markdown("""
            <div class='success-card'>
                <h4>Cash Inflow Positive</h4>
                <p>The business is currently cash-flow positive. Operational revenue is sufficient to sustain current expense structures without draining reserves.</p>
            </div>
            """, unsafe_allow_html=True)
        elif runway_val < 6:
            st.markdown(f"""
            <div class='warning-card'>
                <h4>Critical Runway Alert</h4>
                <p>Remaining Runway: <strong>{runway_val:.1f} Months</strong></p>
                <p>Cash reserves will be fully exhausted within 6 months. Action required: Optimize operational costs or speed up invoicing.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='highlight-card'>
                <h4>Safe Operational Buffer</h4>
                <p>Remaining Runway: <strong>{runway_val:.1f} Months</strong></p>
                <p>Your current cash reserves are stable, allowing sufficient runway for growth or capital raising operations.</p>
            </div>
            """, unsafe_allow_html=True)
            
    with col_t3_right:
        # Plotly chart showing historical and forecasted cash balance (Blue Theme)
        history_df = financials["Cash_Trend"]
        forecast_df = forecasting_data["Forecasts"]
        
        # Combine into a single chart
        fig_fore = go.Figure()
        
        # Historical cash trend
        fig_fore.add_trace(go.Scatter(
            x=history_df["Date"],
            y=history_df["Cumulative_Cash"],
            mode="lines+markers",
            name="Historical Cash Balance",
            line=dict(color="#1d4ed8", width=3)  # Dark Blue
        ))
        
        # Forecasted cash trend
        forecast_dates = forecast_df["Months"]
        f_dates_extended = [history_df["Date"].iloc[-1]] + list(forecast_dates)
        f_cash_extended = [history_df["Cumulative_Cash"].iloc[-1]] + list(forecast_df["Cash"])
        
        fig_fore.add_trace(go.Scatter(
            x=f_dates_extended,
            y=f_cash_extended,
            mode="lines+markers",
            name="Projected Cash (6-Month Forecast)",
            line=dict(color="#60a5fa", width=3, dash="dash")  # Light Blue
        ))
        
        fig_fore.update_layout(
            title="Cash Reserve Forecast & Solvency Outlook",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#0f172a",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(15,23,42,0.06)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0)
        )
        st.plotly_chart(fig_fore, use_container_width=True)

# ==================== TAB 4: TAX PLANNER & OPTIMIZER ====================
with tab4:
    st.markdown("### Tax Assessment & Smart Minimizer")
    st.write("Dynamic calculation of sales tax (GST/VAT) and structural corporate income taxes.")
    
    col_t4_1, col_t4_2 = st.columns(2)
    
    with col_t4_1:
        st.markdown("#### GST / Sales Tax Breakdown")
        
        gst_df = pd.DataFrame({
            "GST Component": [
                "GST Collected on Invoices (Output GST @ 18%)",
                "GST Claimable Credits on Vendors (Input GST/ITC @ 18%)",
                "Net GST Payable to Government"
            ],
            "Amount": [
                f"₹{tax_data['Output_GST']:,.2f}",
                f"₹{tax_data['Input_GST_ITC']:,.2f}",
                f"₹{tax_data['Net_GST_Payable']:,.2f}"
            ]
        })
        st.table(gst_df)
        
        st.write("")
        st.markdown("#### Income Tax Liability")
        it_info = tax_data['Income_Tax']
        
        it_rows = []
        for k, v in it_info.items():
            if k == "Slab Breakdown":
                continue
            if isinstance(v, (int, float)):
                it_rows.append((k, f"₹{v:,.2f}"))
            else:
                it_rows.append((k, str(v)))
                
        it_tbl_df = pd.DataFrame(it_rows, columns=["Metric", "Value"])
        st.table(it_tbl_df)
        
        if "Slab Breakdown" in it_info and len(it_info["Slab Breakdown"]) > 0:
            with st.expander("View Slab Wise Tax Calculation"):
                for slab in it_info["Slab Breakdown"]:
                    st.write(slab)
                    
    with col_t4_2:
        st.markdown("#### AI Tax Optimization Recommendations")
        st.write("Specific, statutory tax deductions identified from your bookkeeping logs:")
        
        recs = get_tax_savings_recommendations(df_transactions, business_type)
        
        for rec in recs:
            impact_badge = f"<span style='color: #22c55e; font-weight: 600;'>{rec.get('impact', 'Medium')}</span>"
            st.markdown(f"""
            <div class='highlight-card'>
                <div style='display: flex; justify-content: space-between;'>
                    <strong>{rec['title']}</strong>
                    <span>Impact: {impact_badge}</span>
                </div>
                <p style='margin-top: 8px; font-size: 0.92rem; color: #334155; line-height: 1.4;'>
                    {rec['description']}
                </p>
            </div>
            """, unsafe_allow_html=True)

# ==================== TAB 5: TALK TO AI CA ====================
with tab5:
    st.markdown("### Consult Zenith AI Senior Chartered Accountant")
    st.write("Chat with an autonomous agent possessing deep expertise in corporate finance, audits, and taxation.")
    
    # Initialize Chatbot
    chatbot = AIChatbot(financials, tax_data, audit_findings, forecasting_data, business_type)
    
    # Chat state initialization (No emojis in welcome text)
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"""Hello! I am Zenith CA, your AI-powered Chartered Accountant. I have analyzed your bookkeeping logs, sales ledger, and overhead expenses. 
            
I'm ready to advise you on how to optimize your operations, reduce your tax liability under statutory laws, explain anomaly triggers, and map your company's solvency runway.

Quick Consultation Topics:
* "How can I reduce my tax liability?"
* "Are there any anomalies or red flags in my books?"
* "What is my cash runway and burn rate?"
* "Explain GSTR-2B Input tax credit claiming instructions."
            
What financial advice do you need today?"""
        })
        
    # Quick action buttons/chips (No emojis)
    chip_col1, chip_col2, chip_col3, chip_col4 = st.columns(4)
    quick_prompt = None
    
    with chip_col1:
        if st.button("How to save tax?"):
            quick_prompt = "How can I reduce my tax liability?"
    with chip_col2:
        if st.button("Check audit flags?"):
            quick_prompt = "Are there any anomalies or red flags in my books?"
    with chip_col3:
        if st.button("Calculate Runway?"):
            quick_prompt = "What is my cash runway and burn rate?"
    with chip_col4:
        if st.button("GST Claim Guide?"):
            quick_prompt = "Explain GSTR-2B Input tax credit claiming instructions."

    # Render previous messages
    for msg in st.session_state.messages:
        role_class = "user-bubble" if msg["role"] == "user" else "assistant-bubble"
        speaker = "You" if msg["role"] == "user" else "Zenith CA"
        st.markdown(f"""
        <div class='{role_class}'>
            <strong>{speaker}:</strong><br>
            {msg['content']}
        </div>
        """, unsafe_allow_html=True)
        
    # React to user input (via either standard box or quick prompt chip)
    user_input = st.chat_input("Ask a financial, tax, or audit question...")
    
    if quick_prompt:
        user_input = quick_prompt
        
    if user_input:
        # User message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Advisor response
        response = chatbot.respond(user_input)
        response_md = response.replace("\n", "  \n")
        st.session_state.messages.append({"role": "assistant", "content": response_md})
        
        # Rerun to render
        st.rerun()
