import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def audit_transactions(df):
    """Audits transactions to find anomalies, duplicates, and suspicious activities.
    Returns a dataframe of findings with severity levels (High, Medium, Low) and audit remarks.
    """
    if len(df) == 0:
        return pd.DataFrame()
        
    audit_findings = []
    
    # 1. Isolation Forest for overall outlier detection on amount
    # Fit isolation forest per category where possible, otherwise globally
    df_features = df[["Amount"]].copy()
    
    # Isolation Forest
    clf = IsolationForest(contamination=0.04, random_state=42)
    df_features["anomaly_score"] = clf.fit_predict(df_features)
    
    # 2. Check for duplicate billing (same amount, category, and close date within 2 days)
    df_sorted = df.sort_values(by=["Amount", "Category", "Date"])
    duplicates = []
    for i in range(len(df_sorted) - 1):
        row1 = df_sorted.iloc[i]
        row2 = df_sorted.iloc[i+1]
        
        # Check if amount and category match and date difference is <= 2 days
        date_diff = abs((row1["Date"] - row2["Date"]).days)
        if row1["Amount"] == row2["Amount"] and row1["Category"] == row2["Category"] and date_diff <= 2:
            # Avoid duplicate warnings for revenue
            if row1["Category"] != "Revenue":
                duplicates.append(row1["Transaction_ID"])
                duplicates.append(row2["Transaction_ID"])
                
    # 3. Process every transaction to detect multiple risks
    for idx, row in df.iterrows():
        tx_id = row["Transaction_ID"]
        amount = row["Amount"]
        desc = row["Description"].lower()
        category = row["Category"]
        date = row["Date"]
        
        # Anomaly level setup
        is_anomaly = df_features.loc[idx, "anomaly_score"] == -1
        
        # Risk evaluations
        risks = []
        severity = "Low"
        
        # A. Check for Duplicates
        if tx_id in duplicates:
            risks.append("Potential Double-Billing / Duplicate Invoice")
            severity = "High"
            
        # B. Outlier amounts
        if is_anomaly:
            # Verify if it's indeed high (not low)
            category_mean = df[df["Category"] == category]["Amount"].mean()
            if amount > category_mean * 2.5:
                risks.append(f"Abnormally high transaction amount for {category}")
                if severity != "High":
                    severity = "Medium"
                    
        # C. Keyword checks (Tax audit red flags)
        suspicious_keywords = ["cash withdrawal", "atm", "reimbursement", "personal", "gift", "refund", "penalty", "fine", "settlement"]
        matched_kw = [kw for kw in suspicious_keywords if kw in desc]
        if matched_kw:
            risks.append(f"Suspicious keyword found: '{matched_kw[0]}'")
            if severity != "High":
                severity = "Medium"
                
        # D. Weekend checks for professional services or rent
        # In a real audit, weekend transactions for B2B/Corporate software or office space are flagged for verification
        is_weekend = date.weekday() >= 5 # 5 is Saturday, 6 is Sunday
        if is_weekend and category in ["Rent & Office Space", "Payroll & Contractors", "Tax & Legal Fees"]:
            risks.append("Weekend transaction for core business operations")
            # Usually low risk unless combined, keep it low
            
        # E. Round-number transaction (e.g. exactly 10,000, 50,000 - often audited in corporate finance)
        if amount > 1000 and amount % 100 == 0 and amount % 1000 == 0:
            risks.append("Perfect round-sum transaction (frequent auditor flag)")
            
        if risks:
            audit_findings.append({
                "Transaction_ID": tx_id,
                "Date": date,
                "Description": row["Description"],
                "Category": category,
                "Amount": amount,
                "Severity": severity,
                "Remarks": " | ".join(risks)
            })
            
    findings_df = pd.DataFrame(audit_findings)
    if len(findings_df) > 0:
        # Sort by severity: High first, then Medium, then Low
        severity_order = {"High": 0, "Medium": 1, "Low": 2}
        findings_df["severity_rank"] = findings_df["Severity"].map(severity_order)
        findings_df = findings_df.sort_values(by=["severity_rank", "Amount"], ascending=[True, False]).drop(columns=["severity_rank"])
        
    return findings_df
