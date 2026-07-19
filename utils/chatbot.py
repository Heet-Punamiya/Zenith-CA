import re

class AIChatbot:
    def __init__(self, financials, tax_data, audit_findings, forecasting_data, business_type):
        self.financials = financials
        self.tax_data = tax_data
        self.audit_findings = audit_findings
        self.forecasting = forecasting_data
        self.business_type = business_type

    def respond(self, query):
        """Simulates a senior CA consulting session, referencing actual business financials."""
        q = query.lower().strip()
        
        # Extracted variables for easy formatting
        revenue = self.financials["Total_Revenue"]
        expenses = self.financials["Total_Expenses"]
        profit = self.financials["Net_Income"]
        cash = self.financials["Current_Cash"]
        net_gst = self.tax_data["Net_GST_Payable"]
        income_tax = self.tax_data["Income_Tax"].get("Total_Income_Tax Payable", self.tax_data["Income_Tax"].get("Total Income Tax Payable", 0))
        runway = self.forecasting["Runway_Months"]
        burn_rate = self.forecasting["Net_Monthly_Burn"]
        
        # 1. Tax Optimization / How to save tax query
        if any(w in q for w in ["save tax", "reduce tax", "lower tax", "optimize tax", "tax saving", "deduction"]):
            return self._get_tax_savings_advice(revenue, profit, income_tax)
            
        # 2. Runway / Cash Flow / Burn Rate query
        elif any(w in q for w in ["runway", "burn rate", "cash flow", "out of money", "cash balance", "survive", "bank balance"]):
            return self._get_runway_advice(cash, burn_rate, runway)
            
        # 3. Anomaly / Audit / Suspicious transactions query
        elif any(w in q for w in ["anomaly", "audit", "fraud", "suspicious", "duplicate", "red flag", "warning"]):
            return self._get_audit_advice()
            
        # 4. GST / VAT query
        elif any(w in q for w in ["gst", "vat", "input credit", "itc", "invoice credit"]):
            return self._get_gst_advice(net_gst)
            
        # 5. Financial Performance / Health check query
        elif any(w in q for w in ["performance", "health", "how is my business", "profitability", "margin", "p&l", "status"]):
            return self._get_health_check_advice(revenue, expenses, profit)
            
        # 6. Default response incorporating actual financials
        else:
            return f"""As your virtual Chartered Accountant, I've reviewed your accounts. Here is a brief health status based on your question:
            
* **Active Entity:** {self.business_type}
* **Current Cash Balance:** ₹{cash:,.2f}
* **Annual Net Profit:** ₹{profit:,.2f} (Net Margin: {((profit/revenue)*100 if revenue > 0 else 0):.1f}%)
* **Current Est. Tax Obligation:** ₹{income_tax:,.2f}
* **GST Payable (Net):** ₹{net_gst:,.2f}

**How I can help you today:**
1. Ask me "How can I save tax?" to see customized optimization strategies for a *{self.business_type}*.
2. Ask me "Are there any anomalies in my books?" to inspect high-risk audits.
3. Ask me "What is my runway and burn rate?" to analyze operational solvency.
4. Ask me about "GST and Input Tax Credits" to see how to claim refund credits on software and marketing.

Please let me know which area you would like me to deep dive into!"""

    def _get_tax_savings_advice(self, revenue, profit, income_tax):
        advice = f"""### CA Advice: Tax Optimization Strategies for your {self.business_type}

Your current taxable profit is **₹{profit:,.2f}**, with an estimated Income Tax of **₹{income_tax:,.2f}**. Let's legally lower this:

1. **Leverage Presumptive Taxation (Section 44ADA)**:
   Since your revenue is **₹{revenue:,.2f}** (which is under the ₹75 Lakh threshold for professionals), you can declare a flat **50% of revenue as profit (₹{revenue*0.5:,.2f})** and pay tax only on that! If your actual expenses are less than 50%, this is a massive win.
   
2. **Claim Input Tax Credit (ITC)**:
   Ensure your GSTIN is added to all your active subscriptions (AWS, Zoom, Slack, Facebook/Google Ads). You have substantial SaaS/marketing spend; doing this will instantly save you **18% of those expenses** by reclaiming the GST paid as credits.

3. **Asset Depreciation (Section 32)**:
   Did you buy laptops, servers, or office furniture? You can claim a **40% depreciation block write-off** on IT equipment this year, directly lowering taxable profit.

4. **Home Office Deduction**:
   Since you run operations as a {self.business_type}, you can draft a rent agreement to pay rent to yourself/family for office space at home. This shifts taxable income from the business to personal slabs, which may have lower tax rates.
   
5. **Director's Remuneration (If Pvt Ltd)**:
   Instead of taking dividends (which are taxed double: first at company level, then at personal level), pay yourself a Director Salary. It is treated as a business expense, reducing corporate tax liability. Keep personal salary under ₹15 Lakhs to stay in lower slabs in the New Tax Regime."""
        return advice

    def _get_runway_advice(self, cash, burn_rate, runway):
        if runway == float('inf'):
            runway_status = "**Infinite (Profitable!)** your business generates more cash than it burns. This is highly solvent."
            action_plan = "You should deploy this cash into growth (e.g. customer acquisition, product research) or yield-bearing financial instruments like corporate liquid funds to prevent inflation drag."
        else:
            runway_status = f"**{runway:.1f} Months**"
            if runway < 6:
                action_plan = """**CRITICAL RUNWAY WARNING:** You have less than 6 months of cash remaining. 
* **Optimize SaaS Subscriptions:** Audit inactive AWS/Cloud developer instances or unused Slack/Zoom seats.
* **Invoice Factoring / Faster Collections:** Move net-30 clients to net-15 or offer a 2% discount for early invoice payments.
* **De-prioritize non-essential marketing:** Cut experiment ads and focus strictly on high-ROI channels."""
            else:
                action_plan = "Your cash reserves are healthy. Continue maintaining a buffer of 6 months while exploring growth avenues."
                
        advice = f"""### CA Advice: Runway & Cash Solvency Report

* **Current Cash Liquidity:** ₹{cash:,.2f}
* **Current Net Burn Rate (Monthly):** ₹{burn_rate:,.2f}
* **Survival Runway:** {runway_status}

#### Actionable CA Recommendations:
1. {action_plan}
2. **Working Capital Management:** Ensure you keep Accounts Receivable (AR) collections tight. Currently, credit extended to customers is holding up cash flow. Set automated payment reminders 3 days before invoices are due."""
        return advice

    def _get_audit_advice(self):
        high_risk = self.audit_findings[self.audit_findings["Severity"] == "High"]
        med_risk = self.audit_findings[self.audit_findings["Severity"] == "Medium"]
        
        if len(self.audit_findings) == 0:
            return "### CA Audit: Clear Opinion\n\nExcellent bookkeeping! I analyzed all transactions using an Isolation Forest ML model and statistical filters. **Zero anomalies, potential double-billings, or suspicious keywords were found.** Your ledger is ready for official audit filing."
            
        advice = f"""### CA Audit: Forensic Anomaly Log
 
I have scanned your transactions. Here are the flags that require immediate attention to prevent audit penalties or fraud:

* **High Risk Alerts:** {len(high_risk)} transactions flagged (potential fraud or double payments)
* **Medium Risk Alerts:** {len(med_risk)} transactions flagged (abnormal amounts / audit triggers)

#### Priority Action Items:
"""
        
        # Print top high/medium alerts
        for idx, row in self.audit_findings.head(5).iterrows():
            badge = "HIGH" if row["Severity"] == "High" else "MED"
            advice += f"\n* **{badge}** | *{row['Date']}* | **₹{row['Amount']:,.2f}** | *{row['Description']}*\n  * **Auditor Flag:** {row['Remarks']}\n"
            
        advice += """\n#### Rectification Steps:
1. **For Double-Billing Flags:** Crosscheck invoice numbers in your accounting portal. If duplicate, request a Credit Note (Debit Note) from the supplier to balance the books.
2. **For Suspicious Keywords:** Ensure proper bills/receipts are uploaded for any cash withdrawals or personal reimbursements. The Income Tax Department frequently disallows personal expenses under Section 37."""
        return advice

    def _get_gst_advice(self, net_gst):
        advice = f"""### CA Advice: GST & Input Tax Credit (ITC) Reclaim

Your current net GST payable for the period is **₹{net_gst:,.2f}**. 

#### How this works:
* **Output GST (Collected):** GST you charged on client invoices.
* **Input GST (Credit):** GST you paid to suppliers (AWS, Rent, Office Utilities, Ads).
* **Net Payable:** Output GST minus Input GST.

#### Optimization Action Plan:
1. **Reclaim Vendor GSTIN Credits:** If you aren't seeing enough Input GST credits, it's because your vendors are filing under a generic/consumer account. 
   * Contact **AWS billing**, **Google Ads billing**, and your **office landlord** and provide your corporate GSTIN.
   * They will issue a revised Tax Invoice. Once they file their GSTR-1, the credit will appear in your **GSTR-2B**, automatically lowering your Net GST payable to zero or creating a refund pool.
2. **GST Filing Calendar Reminder:**
   * **GSTR-1 (Outward Supplies):** Due by the 11th of every succeeding month.
   * **GSTR-3B (Summary & Payment):** Due by the 20th of every succeeding month. Ensure payments are done on time to avoid interest charges (18% per annum)."""
        return advice

    def _get_health_check_advice(self, revenue, expenses, profit):
        margin = (profit / revenue * 100) if revenue > 0 else 0
        status = "HEALTHY" if profit > 0 and margin > 15 else "MARGINAL" if profit > 0 else "UNHEALTHY (Operating Loss)"
        
        advice = f"""### CA Advice: Financial Health & Profitability Check

* **Revenue Performance:** ₹{revenue:,.2f}
* **Operational Expense Burn:** ₹{expenses:,.2f}
* **Net Profit:** ₹{profit:,.2f}
* **Net Profit Margin:** {margin:.2f}%
* **Overall Status:** **{status}**

#### Financial Ratios Analysis:
1. **Operating Margin:** Your margin is **{margin:.2f}%**. A margin above 20% is excellent for services/SaaS. If below 10%, you have a pricing model or cost control issue.
2. **Operating Efficiency:** For every ₹100 earned, you spend ₹{(expenses/revenue*100 if revenue > 0 else 100):.1f} on expenses.
3. **Expense Optimization Target:** Look at your highest category expense in the dashboard. If it is Payroll or Software, consider outsourcing low-risk tasks or optimizing server instances to widen your profit margins."""
        return advice
