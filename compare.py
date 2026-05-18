import pandas as pd
from calculator import calculate_totals


def compare_loans(loans):
    results = []

    for loan in loans:
        principal = loan["principal"]
        rate = loan["rate"]
        months = loan["months"]
        name = loan["name"]

        totals = calculate_totals(principal, rate, months)

        results.append({
            "Loan Option": name,
            "Principal": round(principal, 2),
            "Rate (%)": rate,
            "Months": months,
            "EMI": round(totals["emi"], 2),
            "Total Repayment": round(totals["total_payment"], 2),
            "Total Interest": round(totals["total_interest"], 2)
        })

    return pd.DataFrame(results)


def best_loan_by_interest(comparison_df):
    best_row = comparison_df.loc[comparison_df["Total Interest"].idxmin()]
    return best_row["Loan Option"]