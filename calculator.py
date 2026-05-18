def calculate_emi(principal, annual_rate, months):
    monthly_rate = annual_rate / 12 / 100

    if months <= 0:
        return 0.0

    if monthly_rate == 0:
        return principal / months

    emi = principal * monthly_rate * (1 + monthly_rate) ** months / ((1 + monthly_rate) ** months - 1)
    return emi


def calculate_totals(principal, annual_rate, months):
    emi = calculate_emi(principal, annual_rate, months)
    total_payment = emi * months
    total_interest = total_payment - principal

    return {
        "emi": emi,
        "total_payment": total_payment,
        "total_interest": total_interest
    }