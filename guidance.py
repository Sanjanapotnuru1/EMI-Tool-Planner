def generate_guidance(emi, monthly_income, total_interest, principal, months):
    suggestions = []

    if monthly_income and monthly_income > 0:
        ratio = (emi / monthly_income) * 100

        if ratio <= 30:
            suggestions.append(
                f"Your EMI is about {ratio:.1f}% of your monthly income, which is generally manageable."
            )
        elif ratio <= 45:
            suggestions.append(
                f"Your EMI is about {ratio:.1f}% of your monthly income, so you should plan your expenses carefully."
            )
        else:
            suggestions.append(
                f"Your EMI is about {ratio:.1f}% of your monthly income, which may be financially risky."
            )

    interest_ratio = (total_interest / principal) * 100 if principal else 0

    if interest_ratio < 25:
        suggestions.append("This loan has a relatively low total interest burden.")
    elif interest_ratio < 60:
        suggestions.append("This loan has a moderate interest burden over the full tenure.")
    else:
        suggestions.append("This loan has a high total interest burden, so choosing a shorter tenure may reduce overall cost.")

    if months > 120:
        suggestions.append("A longer tenure lowers EMI but increases the total interest significantly.")
    elif months < 36:
        suggestions.append("A shorter tenure reduces total interest, but the monthly EMI becomes higher.")

    return suggestions