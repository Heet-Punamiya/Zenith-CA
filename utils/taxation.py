import pandas as pd
import numpy as np

def calculate_taxes(df, business_type="Sole Proprietorship", annual_salary_drawn=0.0):
    """Calculates GST obligations, estimated Corporate/Individual Income Tax,
    and provides a breakdown of tax liability and credits.
    """
    # 1. GST Calculation (Standard 18% for B2B/Tech/Consulting)
    # Output GST: 18% on Revenue (Income)
    revenue_df = df[df["Type"] == "Income"]
    total_revenue = revenue_df["Amount"].sum()
    output_gst = np.round(total_revenue * 0.18, 2)
    
    # Input GST (ITC): 18% on GST-eligible expenses (Software, Rent, Utilities, Marketing)
    # Not eligible: Payroll, Tax & Legal, Travel (flights are, but let's keep it simple), Misc
    itc_eligible_categories = ["Software & Infrastructure", "Marketing & Advertising", "Utilities & Internet", "Rent & Office Space"]
    itc_expense_df = df[(df["Type"] == "Expense") & (df["Category"].isin(itc_eligible_categories))]
    total_itc_expenses = itc_expense_df["Amount"].sum()
    input_gst_itc = np.round(total_itc_expenses * 0.18, 2)
    
    net_gst_payable = max(0.0, np.round(output_gst - input_gst_itc, 2))
    
    # 2. Income Tax Calculation
    # Taxable Income = Total Revenue - Total Expenses (excluding tax provision itself)
    expense_df = df[df["Type"] == "Expense"]
    total_expenses = expense_df["Amount"].sum()
    net_profit = total_revenue - total_expenses
    taxable_profit = max(0.0, net_profit)
    
    tax_details = {}
    
    if business_type == "Sole Proprietorship":
        # Uses Slab Rates. Let's use Indian New Tax Regime (FY 2024-25 / AY 2025-26)
        # Up to 3L: Nil
        # 3L - 6L: 5%
        # 6L - 9L: 10%
        # 9L - 12L: 15%
        # 12L - 15L: 20%
        # Above 15L: 30%
        # Plus 4% Cess
        
        income = taxable_profit
        tax_before_cess = 0.0
        
        slabs = [
            (300000, 0.00),
            (300000, 0.05),
            (300000, 0.10),
            (300000, 0.15),
            (300000, 0.20),
            (float('inf'), 0.30)
        ]
        
        remaining_income = income
        breakdown = []
        
        for slab_limit, rate in slabs:
            if remaining_income <= 0:
                break
            taxable_in_slab = min(remaining_income, slab_limit)
            slab_tax = taxable_in_slab * rate
            tax_before_cess += slab_tax
            remaining_income -= taxable_in_slab
            if rate > 0:
                breakdown.append(f"Slab {int(rate*100)}%: ₹{taxable_in_slab:,.2f} -> Tax: ₹{slab_tax:,.2f}")
                
        cess = np.round(tax_before_cess * 0.04, 2)
        total_income_tax = np.round(tax_before_cess + cess, 2)
        
        tax_details = {
            "Taxable Profit": taxable_profit,
            "Regime": "New Tax Regime (FY 2024-25)",
            "Base Tax": tax_before_cess,
            "Health & Education Cess (4%)": cess,
            "Total Income Tax Payable": total_income_tax,
            "Effective Tax Rate": f"{np.round((total_income_tax / taxable_profit * 100), 2) if taxable_profit > 0 else 0.0}%",
            "Slab Breakdown": breakdown
        }
        
    elif business_type == "Partnership Firm / LLP":
        # Flat 30% tax rate + 4% cess = 31.2% effective tax rate
        base_tax = np.round(taxable_profit * 0.30, 2)
        cess = np.round(base_tax * 0.04, 2)
        total_income_tax = np.round(base_tax + cess, 2)
        
        tax_details = {
            "Taxable Profit": taxable_profit,
            "Rate": "30% Flat Rate",
            "Base Tax": base_tax,
            "Health & Education Cess (4%)": cess,
            "Total Income Tax Payable": total_income_tax,
            "Effective Tax Rate": "31.2%"
        }
        
    else: # Private Limited Company (Pvt Ltd)
        # Flat 22% (Section 115BAA) or 25% (turnover < 400Cr)
        # Let's say 22% base + 10% surcharge + 4% cess = 25.17% effective rate
        base_tax = np.round(taxable_profit * 0.22, 2)
        surcharge = np.round(base_tax * 0.10, 2)
        cess = np.round((base_tax + surcharge) * 0.04, 2)
        total_income_tax = np.round(base_tax + surcharge + cess, 2)
        
        tax_details = {
            "Taxable Profit": taxable_profit,
            "Rate": "22% Base Rate (Sec 115BAA)",
            "Base Tax": base_tax,
            "Surcharge (10%)": surcharge,
            "Health & Education Cess (4%)": cess,
            "Total Income Tax Payable": total_income_tax,
            "Effective Tax Rate": "25.17%"
        }
        
    return {
        "Output_GST": output_gst,
        "Input_GST_ITC": input_gst_itc,
        "Net_GST_Payable": net_gst_payable,
        "Income_Tax": tax_details
    }

def get_tax_savings_recommendations(df, business_type):
    """Analyzes the current accounts and provides action items to legally minimize tax."""
    recommendations = []
    
    # Check 1: Input Tax Credit (ITC) maximization
    # Estimate if expenses have missing GST detail
    non_gst_registered_expenses = df[(df["Type"] == "Expense") & (df["Category"].isin(["Software & Infrastructure", "Marketing & Advertising"])) & (df["Amount"] > 2000)]
    if len(non_gst_registered_expenses) > 0:
        recommendations.append({
            "title": "Claim Unused Input Tax Credit (ITC)",
            "impact": "High (Saves 18% on SaaS & Ads)",
            "description": f"You spent ₹{non_gst_registered_expenses['Amount'].sum():,.2f} on software/marketing. Ensure you add your GSTIN to profiles (AWS, Google, Facebook) to claim 18% GST refund as credit."
        })
        
    # Check 2: Depreciation on Assets
    # Equipment / hardware assets can be depreciated
    misc_hardware = df[df["Description"].str.contains("computer|laptop|macbook|furniture|desk|monitor|phone", case=False)]
    if len(misc_hardware) > 0:
        asset_sum = misc_hardware["Amount"].sum()
        depreciation_saving = asset_sum * 0.40 # 40% depreciation for computers in India
        recommendations.append({
            "title": "Apply 40% Block Depreciation on Laptops/IT Assets",
            "impact": "Medium (Reduces taxable income)",
            "description": f"Identified ₹{asset_sum:,.2f} spent on computer/hardware. Claiming 40% depreciation under Section 32 allows you to write off ₹{depreciation_saving:,.2f} from this year's taxable profit."
        })
        
    # Check 3: Director/Partner Salary vs Dividends (Pvt Ltd)
    if business_type == "Private Limited Company (Pvt Ltd)":
        recommendations.append({
            "title": "Optimize Director Remuneration vs Corporate Tax",
            "impact": "High",
            "description": "Company profits are taxed at 25.17%. Paying directors a salary counts as a business expense, reducing corporate tax. However, personal tax rates apply to directors. Keep director salary up to ₹15 Lakhs (New Regime slab limit) to minimize overall tax leakage."
        })
        
    # Check 4: Rent to self (Proprietorship/Partnership)
    office_rent = df[df["Category"] == "Rent & Office Space"]
    if len(office_rent) == 0:
        recommendations.append({
            "title": "Rent home office space to your business",
            "impact": "Medium",
            "description": "If operating from home, establish a lease agreement between you and your business. The rental payments are a deductible expense for the business, shifting income to a lower personal slab or utilizing basic exemptions."
        })
        
    # Check 5: Section 80C/80D deductions (Sole Proprietor)
    if business_type == "Sole Proprietorship":
        recommendations.append({
            "title": "Utilize Section 80C and 80D limits",
            "impact": "Medium (Saves up to ₹50,000 in tax)",
            "description": "Ensure you invest up to ₹1.5 Lakhs in PPF, ELSS Mutual Funds, or NPS under Sec 80C, and buy health insurance for yourself and parents under Sec 80D (deduction up to ₹75,000)."
        })
        
    # General Check 6: Presumptive Taxation (Section 44ADA / 44AD)
    total_rev = df[df["Type"] == "Income"]["Amount"].sum()
    if total_rev <= 7500000: # 75 Lakh limit for 44ADA (professionals)
        recommendations.append({
            "title": "Evaluate Section 44ADA Presumptive Taxation",
            "impact": "Very High (Saves accounting fees & simplifies tax)",
            "description": f"As a professional service with turnover of ₹{total_rev:,.2f} (< ₹75L), you can declare only 50% of revenue as taxable profit. This eliminates the need for detailed bookkeeping audits and reduces taxable income to ₹{total_rev*0.5:,.2f}."
        })
        
    return recommendations
