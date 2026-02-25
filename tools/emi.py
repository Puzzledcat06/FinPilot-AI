"""
EMI Calculator Tool — Pure deterministic math, no LLM.
"""


def calculate_emi(principal: float, annual_rate: float, tenure_years: int) -> dict:
    """
    Calculate Equated Monthly Installment (EMI).

    Args:
        principal: Loan amount in currency units.
        annual_rate: Annual interest rate in percentage (e.g. 11 for 11%).
        tenure_years: Loan tenure in years.

    Returns:
        dict with emi, total_payment, total_interest, tenure_months.
    """
    if principal <= 0:
        raise ValueError("Loan principal must be positive.")
    if annual_rate < 0:
        raise ValueError("Interest rate cannot be negative.")
    if tenure_years <= 0:
        raise ValueError("Tenure must be at least 1 year.")

    tenure_months = tenure_years * 12

    if annual_rate == 0:
        emi = principal / tenure_months
        total_payment = principal
        total_interest = 0.0
    else:
        monthly_rate = (annual_rate / 100) / 12
        emi = principal * monthly_rate * ((1 + monthly_rate) ** tenure_months) / (
            ((1 + monthly_rate) ** tenure_months) - 1
        )
        total_payment = emi * tenure_months
        total_interest = total_payment - principal

    return {
        "emi": round(emi, 2),
        "total_payment": round(total_payment, 2),
        "total_interest": round(total_interest, 2),
        "tenure_months": tenure_months,
        "principal": principal,
        "annual_rate": annual_rate,
    }
