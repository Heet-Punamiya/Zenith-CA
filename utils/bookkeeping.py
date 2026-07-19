import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
import datetime

# Pre-defined categories for bookkeeping classification
CATEGORIES = [
    "Revenue",
    "Marketing & Advertising",
    "Software & Infrastructure",
    "Travel & Lodging",
    "Rent & Office Space",
    "Payroll & Contractors",
    "Utilities & Internet",
    "Tax & Legal Fees",
    "Miscellaneous Expense"
]

# Training data to teach the ML model how to categorize transactions
TRAINING_DATA = [
    # Revenue
    ("Invoice payment from client Acme Corp", "Revenue"),
    ("Stripe payout for SaaS subscriptions", "Revenue"),
    ("Consulting services invoice payment", "Revenue"),
    ("Product sales payout on Shopify", "Revenue"),
    ("Wire transfer from customer BigCo LLC", "Revenue"),
    ("Subscription renewal fee payment received", "Revenue"),
    
    # Marketing
    ("Google Ads PPC advertising campaign", "Marketing & Advertising"),
    ("Facebook Ads manager invoice billing", "Marketing & Advertising"),
    ("Sponsorship newsletter promotion", "Marketing & Advertising"),
    ("LinkedIn Ads marketing campaigns", "Marketing & Advertising"),
    ("SEO consulting and content marketing", "Marketing & Advertising"),
    
    # Software & Infrastructure
    ("Amazon Web Services AWS cloud hosting", "Software & Infrastructure"),
    ("GitHub team subscription billing", "Software & Infrastructure"),
    ("Slack Technologies team chat subscription", "Software & Infrastructure"),
    ("Zoom Video Communications monthly bill", "Software & Infrastructure"),
    ("OpenAI API developer usage billing", "Software & Infrastructure"),
    ("Vercel hosting platform hosting charges", "Software & Infrastructure"),
    ("Google Workspace email suite", "Software & Infrastructure"),
    
    # Travel
    ("Uber trip ride sharing fare", "Travel & Lodging"),
    ("Delta Airlines flight booking business trip", "Travel & Lodging"),
    ("Marriott Hotel booking business conference", "Travel & Lodging"),
    ("Lyft ride home from airport", "Travel & Lodging"),
    ("Train ticket booking for client meeting", "Travel & Lodging"),
    
    # Rent & Office
    ("Monthly office space lease payment rent", "Rent & Office Space"),
    ("WeWork co-working hot desk monthly rent", "Rent & Office Space"),
    ("Office cleaning services monthly charge", "Rent & Office Space"),
    ("Office furniture chairs and desks purchase", "Rent & Office Space"),
    
    # Payroll
    ("Monthly salary payout to employee John Doe", "Payroll & Contractors"),
    ("Contractor invoice payment web development", "Payroll & Contractors"),
    ("Freelancer design work logo design payment", "Payroll & Contractors"),
    ("ADP payroll processing fees and wages", "Payroll & Contractors"),
    ("Bonus payment to sales team manager", "Payroll & Contractors"),
    
    # Utilities
    ("ConEd electric utility bill office power", "Utilities & Internet"),
    ("Comcast Business internet and phone bill", "Utilities & Internet"),
    ("Water utility bill office building", "Utilities & Internet"),
    ("Waste management office trash disposal", "Utilities & Internet"),
    
    # Tax & Legal
    ("Corporate annual filing fees registry", "Tax & Legal Fees"),
    ("Legal consultation fee contract review", "Tax & Legal Fees"),
    ("Trademark registration application attorney", "Tax & Legal Fees"),
    ("State tax franchise tax annual payment", "Tax & Legal Fees"),
    
    # Miscellaneous
    ("Office snacks groceries supermarket", "Miscellaneous Expense"),
    ("Coffee machine capsules and cups", "Miscellaneous Expense"),
    ("Team dinner restaurant celebration", "Miscellaneous Expense"),
    ("Lost keys replacement locksmith fee", "Miscellaneous Expense")
]

class TransactionClassifier:
    def __init__(self):
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), stop_words='english')),
            ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
        ])
        self.fit_model()

    def fit_model(self):
        texts, labels = zip(*TRAINING_DATA)
        self.pipeline.fit(texts, labels)

    def predict(self, descriptions):
        """Predict categories for a list of descriptions."""
        if isinstance(descriptions, str):
            descriptions = [descriptions]
        return self.pipeline.predict(descriptions)

    def predict_proba(self, descriptions):
        """Predict probability scores for verification/auditing."""
        if isinstance(descriptions, str):
            descriptions = [descriptions]
        probs = self.pipeline.predict_proba(descriptions)
        classes = self.pipeline.classes_
        results = []
        for prob in probs:
            results.append({classes[i]: float(prob[i]) for i in range(len(classes))})
        return results

def generate_mock_transactions(num_transactions=150, seed=42):
    """Generates realistic transaction logs for a business over the past 12 months."""
    np.random.seed(seed)
    current_date = datetime.date.today()
    start_date = current_date - datetime.timedelta(days=365)
    
    dates = []
    descriptions = []
    amounts = []
    tx_types = []
    
    # Generate structured business transactions
    # Regular monthly expenses
    for month in range(12):
        tx_date = start_date + datetime.timedelta(days=month * 30 + np.random.randint(-2, 3))
        
        # Office Rent
        dates.append(tx_date)
        descriptions.append("Office lease monthly rent payment")
        amounts.append(5000.00)
        tx_types.append("Expense")
        
        # Payroll
        dates.append(tx_date + datetime.timedelta(days=5))
        descriptions.append("Employee payroll wages disbursement ADP")
        amounts.append(18500.00)
        tx_types.append("Expense")
        
        # Internet & Phone
        dates.append(tx_date + datetime.timedelta(days=10))
        descriptions.append("Comcast Business broadband internet & VoIP bill")
        amounts.append(250.00)
        tx_types.append("Expense")
        
        # Electric & Utilities
        dates.append(tx_date + datetime.timedelta(days=12))
        descriptions.append("Electric utility bill office power ConEd")
        amounts.append(380.00)
        tx_types.append("Expense")
        
        # AWS cloud
        dates.append(tx_date + datetime.timedelta(days=15))
        descriptions.append(f"Amazon Web Services AWS Cloud Hosting Invoice {np.random.randint(100000, 999999)}")
        amounts.append(np.round(1200.00 + np.random.normal(0, 150), 2))
        tx_types.append("Expense")
        
        # Slack / Zoom
        dates.append(tx_date + datetime.timedelta(days=18))
        descriptions.append("Slack Technologies monthly communication subscription")
        amounts.append(180.00)
        tx_types.append("Expense")
        
        dates.append(tx_date + datetime.timedelta(days=19))
        descriptions.append("Zoom Video monthly conference license renewal")
        amounts.append(79.00)
        tx_types.append("Expense")

    # Generate random transactions (Income and other Expenses)
    # Increased income amounts to simulate a highly profitable, successful enterprise
    other_descriptions = [
        ("Invoice payment received Client Acme Corp", 45000.00, "Income"),
        ("Stripe SaaS subscription revenue payout", 52000.00, "Income"),
        ("Consulting services milestone payment TechStart", 28000.00, "Income"),
        ("Shopify store sales revenue payout", 22000.00, "Income"),
        ("Invoice payment received Zenith Agency Ltd", 38000.00, "Income"),
        ("Google Ads pay-per-click marketing campaign", 1500.00, "Expense"),
        ("Facebook Ads advertising billing manager", 2000.00, "Expense"),
        ("Uber business ride taxi fare", 35.50, "Expense"),
        ("Delta Airlines roundtrip flight sales conference", 680.00, "Expense"),
        ("Marriott Hotel stay sales conference team", 450.00, "Expense"),
        ("Office snacks groceries and drinks restocking", 120.40, "Expense"),
        ("Contractor invoice payment Python backend developer", 3500.00, "Expense"),
        ("Corporate annual filing registry fee Secretary of State", 150.00, "Expense"),
        ("Legal consultation contract review Law Offices LLP", 800.00, "Expense"),
        ("LinkedIn premium recruiting subscription team", 150.00, "Expense"),
        ("OpenAI API monthly developer credits", 340.00, "Expense")
    ]
    
    remaining = num_transactions - len(dates)
    for _ in range(remaining):
        # Pick random item from descriptions with varying amounts
        desc_template, base_amount, ttype = other_descriptions[np.random.randint(len(other_descriptions))]
        
        # Random date in the year
        rand_days = np.random.randint(0, 365)
        tx_date = start_date + datetime.timedelta(days=rand_days)
        
        dates.append(tx_date)
        descriptions.append(desc_template)
        # Add random noise to amounts
        noise = np.random.uniform(0.8, 1.25)
        amounts.append(np.round(base_amount * noise, 2))
        tx_types.append(ttype)
        
    df = pd.DataFrame({
        "Date": dates,
        "Description": descriptions,
        "Amount": amounts,
        "Type": tx_types
    })
    
    # Sort by Date
    df = df.sort_values(by="Date").reset_index(drop=True)
    df["Transaction_ID"] = [f"TX-{1000 + i}" for i in range(len(df))]
    
    # Add predicted Category using our ML model
    clf = TransactionClassifier()
    df["Category"] = clf.predict(df["Description"].tolist())
    
    # Ensure revenue transactions are set to Revenue category
    df.loc[df["Type"] == "Income", "Category"] = "Revenue"
    # Ensure rent is Rent
    df.loc[df["Description"].str.contains("rent|lease", case=False), "Category"] = "Rent & Office Space"
    # Ensure payroll is Payroll
    df.loc[df["Description"].str.contains("payroll|salary|wages", case=False), "Category"] = "Payroll & Contractors"
    
    return df

def calculate_financials(df):
    """Calculates general ledger, P&L, Balance Sheet estimates, Cash Flow metrics."""
    # Group by category and type
    revenue_df = df[df["Category"] == "Revenue"]
    expense_df = df[df["Category"] != "Revenue"]
    
    total_revenue = revenue_df["Amount"].sum()
    total_expenses = expense_df["Amount"].sum()
    net_income = total_revenue - total_expenses
    
    # Group expenses by Category
    category_breakdown = expense_df.groupby("Category")["Amount"].sum().reset_index()
    category_breakdown = category_breakdown.sort_values(by="Amount", ascending=False)
    
    # Cash flow calculations
    # Starting balance is 500,000 (realistic for our higher revenues)
    initial_cash = 500000.00
    df_sorted = df.sort_values(by="Date").copy()
    df_sorted["Flow"] = df_sorted.apply(lambda r: r["Amount"] if r["Type"] == "Income" else -r["Amount"], axis=1)
    df_sorted["Cumulative_Cash"] = initial_cash + df_sorted["Flow"].cumsum()
    
    current_cash = df_sorted["Cumulative_Cash"].iloc[-1]
    
    # Balance Sheet based on typical asset ratios
    ar = np.round(total_revenue * 0.08, 2)
    equipment = 25000.00
    total_assets = current_cash + ar + equipment
    
    # Liabilities: Accounts Payable ~ 4% of expenses. Unpaid taxes.
    ap = np.round(total_expenses * 0.04, 2)
    tax_provision = np.round(max(0.0, net_income * 0.20), 2)  # 20% tax estimate
    total_liabilities = ap + tax_provision
    
    # Equity
    retained_earnings = net_income
    owner_equity = total_assets - total_liabilities - retained_earnings
    
    balance_sheet = {
        "Assets": {
            "Cash & Cash Equivalents": current_cash,
            "Accounts Receivable": ar,
            "Equipment & Hardware": equipment,
            "Total Assets": total_assets
        },
        "Liabilities": {
            "Accounts Payable": ap,
            "Estimated Tax Provision": tax_provision,
            "Total Liabilities": total_liabilities
        },
        "Equity": {
            "Initial Owner Equity": owner_equity,
            "Retained Earnings": retained_earnings,
            "Total Equity": owner_equity + retained_earnings
        }
    }
    
    return {
        "Total_Revenue": total_revenue,
        "Total_Expenses": total_expenses,
        "Net_Income": net_income,
        "Category_Breakdown": category_breakdown,
        "Current_Cash": current_cash,
        "Balance_Sheet": balance_sheet,
        "Cash_Trend": df_sorted[["Date", "Cumulative_Cash"]]
    }
