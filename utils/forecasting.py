import pandas as pd
import numpy as np
from statsmodels.tsa.api import Holt
import datetime

def forecast_financials(df, forecast_months=6):
    """Forecasts Monthly Revenue, Expenses, and Cash Balance for the next N months.
    Uses Exponential Smoothing with a trend, and falls back to a linear trend model
    if there are fewer than 6 months of historical data.
    """
    # 1. Aggregate data by month
    df = df.copy()
    df["YearMonth"] = df["Date"].apply(lambda x: datetime.date(x.year, x.month, 1))
    
    monthly_data = df.groupby(["YearMonth", "Type"])["Amount"].sum().unstack(fill_value=0)
    
    # Ensure both columns exist
    if "Income" not in monthly_data.columns:
        monthly_data["Income"] = 0.0
    if "Expense" not in monthly_data.columns:
        monthly_data["Expense"] = 0.0
        
    monthly_data = monthly_data.sort_index()
    
    # Calculate Net Cash Flow per month
    monthly_data["Net_Flow"] = monthly_data["Income"] - monthly_data["Expense"]
    
    # Reconstruct cash balance trend month-over-month
    # Starting balance is 50,000
    initial_cash = 50000.00
    monthly_data["Cash_End"] = initial_cash + monthly_data["Net_Flow"].cumsum()
    
    # If the history is extremely short (e.g. less than 3 months), return hardcoded or simple projections
    n_obs = len(monthly_data)
    
    future_months = [
        monthly_data.index[-1] + pd.DateOffset(months=i)
        for i in range(1, forecast_months + 1)
    ]
    # Convert back to date
    future_months = [d.date() for d in future_months]
    
    forecasts = {
        "Months": future_months,
        "Revenue": [],
        "Expenses": [],
        "Cash": []
    }
    
    # Model fitting helper: returns forecast list of length forecast_months
    def get_forecast(series):
        y = series.values
        if len(y) >= 6:
            try:
                # Use Holt's linear trend method
                model = Holt(y, initialization_method="estimated").fit()
                pred = model.forecast(forecast_months)
                # Keep values reasonable (e.g. non-negative for revenue/expenses)
                return [max(0.0, np.round(v, 2)) for v in pred]
            except Exception:
                pass
        
        # Fallback: Simple Linear Trend
        x = np.arange(len(y))
        slope, intercept = np.polyfit(x, y, 1)
        pred = []
        for i in range(len(y), len(y) + forecast_months):
            val = slope * i + intercept
            pred.append(max(0.0, np.round(val, 2)))
        return pred

    forecasts["Revenue"] = get_forecast(monthly_data["Income"])
    forecasts["Expenses"] = get_forecast(monthly_data["Expense"])
    
    # Cash forecast is cumulative cash based on projected net flow
    last_cash = monthly_data["Cash_End"].iloc[-1]
    current_cash = last_cash
    cash_forecast = []
    
    for r, e in zip(forecasts["Revenue"], forecasts["Expenses"]):
        net = r - e
        current_cash += net
        cash_forecast.append(max(0.0, np.round(current_cash, 2)))
        
    forecasts["Cash"] = cash_forecast
    
    # Calculate Runway Metrics
    # Average monthly burn rate over the last 3 months
    recent_months = monthly_data.tail(3)
    avg_recent_expenses = recent_months["Expense"].mean() if len(recent_months) > 0 else 1.0
    avg_recent_income = recent_months["Income"].mean() if len(recent_months) > 0 else 0.0
    
    avg_net_burn = avg_recent_expenses - avg_recent_income
    
    # Runway in months
    if avg_net_burn <= 0:
        runway_months = float('inf') # Profitable, infinite runway!
    else:
        runway_months = last_cash / avg_net_burn
        
    return {
        "Monthly_History": monthly_data.reset_index(),
        "Forecasts": pd.DataFrame(forecasts),
        "Avg_Monthly_Expenses": avg_recent_expenses,
        "Avg_Monthly_Income": avg_recent_income,
        "Net_Monthly_Burn": avg_net_burn,
        "Runway_Months": runway_months
    }
