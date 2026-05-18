import pandas as pd
from calculator import calculate_emi


def generate_schedule(principal, annual_rate, months):
    emi = calculate_emi(principal, annual_rate, months)
    monthly_rate = annual_rate / 12 / 100
    balance = principal
    rows = []

    for month in range(1, months + 1):
        interest = balance * monthly_rate
        principal_paid = emi - interest

        if month == months:
            principal_paid = balance
            emi_paid = principal_paid + interest
        else:
            emi_paid = emi

        balance = max(0, balance - principal_paid)

        rows.append({
            "Month": month,
            "EMI": round(emi_paid, 2),
            "Principal Paid": round(principal_paid, 2),
            "Interest Paid": round(interest, 2),
            "Remaining Balance": round(balance, 2)
        })

    return pd.DataFrame(rows)