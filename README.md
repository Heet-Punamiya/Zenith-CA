# Zenith CA — Autonomous AI Chartered Accountant

Zenith CA is an autonomous, AI-powered Chartered Accountant, Auditor, and Tax Advisor web application. It ingests bookkeeping ledgers or transaction CSV files to perform automated ledger analysis, forensic audit checks, cash flow runway forecasting, slab-wise tax calculations, and provides an interactive AI consult session with custom PDF reporting.

---

## 🚀 Key Modules & Features

### 1. Financial Control Center
* **Bookkeeping Ledger Processor:** Automatically maps, cleans, and parses uploaded bank statements or transaction ledgers (CSV format).
* **AI Categorical Allocation:** Classifies general transactions (such as Revenue, Software & Infrastructure, Payroll, Rent, Marketing, Utilities, etc.) using machine learning.
* **Interactive Dashboards:** 
  * Monthly cash inflow vs. outflow comparison.
  * Operational expense allocation breakdown.
* **Projected Balance Sheet:** Renders simplified double-entry bookkeeping ledgers split into Assets, Liabilities, and Owner's Equity.

### 2. AI Forensic Audit (Fraud Guard)
* **Isolation Forest Anomaly Detection:** Utilizes machine learning models (`scikit-learn` Isolation Forest) to isolate suspicious transaction values or unusual cash outflows.
* **Red Flags & Warning Log:** Automatically logs high and medium-severity audit risks, duplicate billing occurrences, or non-business descriptions.

### 3. Predictive Cash Flow & Solvency Projections
* **Solvency Forecasting:** Models monthly historical burn rates and projects future cash balances up to 6 months using Linear Regression.
* **Capital Runway Health Indicator:** Displays real-time runway status (Infinite/Profitable, Safe Buffer, or Critical Warning) with detailed actions to prevent cash crunches.

### 4. Tax Planner & Smart Minimizer
* **GST / Sales Tax Calculator:** Computes Output GST (collected on revenue) and Input Tax Credits (ITC, claimed on vendor spend) to calculate the net GST payable to the government.
* **Multi-Structure Income Tax Engine:** 
  * **Sole Proprietorship:** Slab-wise tax calculations under the Indian New Tax Regime (0% up to ₹3L, up to 30% above ₹15L, plus 4% Cess).
  * **LLP / Partnership:** Flat 30% tax rate plus 4% Cess (31.2% effective tax rate).
  * **Private Limited Company:** Flat 22% corporate tax rate (Sec 115BAA) plus 10% surcharge and 4% Cess (25.17% effective tax rate).
* **AI Tax Savings Recommendations:** Scans bookkeeping ledgers for tax write-offs, highlighting presumptive tax (Section 44ADA), hardware depreciation (Section 32), rent-to-self, and SaaS input tax credits.

### 5. Zenith AI Chat Agent
* **Context-Aware Consultant:** Allows users to chat directly with an autonomous Chartered Accountant agent that possesses full knowledge of the current company financials.
* **Interactive Prompts:** Quick action chips for rapid consultations regarding tax-saving advice, runway assessments, audit triggers, and GST claim steps.

### 6. Official PDF Exporter
* Compiles all financial metrics, tax breakdowns, forensic audit warnings, and forecasts into a beautifully styled corporate PDF report via `fpdf2`.

---

## 🛠️ Technology Stack

* **Frontend & UI:** [Streamlit](https://streamlit.io/) (responsive layout, interactive charts, sidebar uploader, custom Light & White themes).
* **Data Processing:** [Pandas](https://pandas.pydata.org/) and [NumPy](https://numpy.org/).
* **Data Visualization:** [Plotly](https://plotly.com/) (interactive bar, pie, and line charts).
* **Machine Learning:** [Scikit-Learn](https://scikit-learn.org/) (for Isolation Forest and forecasting models).
* **PDF Engine:** [FPDF2](https://py-pdf.github.io/fpdf2/).
* **Deployment:** [Vercel](https://vercel.com/) (for index API) and [Streamlit Community Cloud](https://streamlit.io/cloud).

---

## 💻 Local Setup & Development

To run the Streamlit application locally:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Heet-Punamiya/Zenith-CA.git
   cd Zenith-CA
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the local Streamlit server:**
   ```bash
   python -m streamlit run app.py
   ```

4. Open your browser and navigate to **[http://localhost:8501](http://localhost:8501)**.
