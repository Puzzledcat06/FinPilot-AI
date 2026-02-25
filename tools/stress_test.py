"""
Stress Test Tool — Simulates interest rate shocks. No LLM.
"""

from tools.emi import calculate_emi
from tools.affordability import check_affordability


def stress_test(
    principal: float,
    annual_rate: float,
    tenure_years: int,
    monthly_salary: float,
    monthly_expenses: float = 0,
    shocks: list[float] | None = None,
) -> list[dict]:
    """
    Simulate interest rate shocks and assess impact on EMI + affordability.

    Args:
        principal: Loan amount.
        annual_rate: Current annual interest rate (%).
        tenure_years: Loan tenure in years.
        monthly_salary: Monthly take-home salary.
        monthly_expenses: Fixed monthly expenses (rent, food, existing EMIs).
        shocks: Rate increases to simulate (in %). Defaults to [+1, +2].

    Returns:
        List of dicts, each with shocked rate, new EMI, affordability, and delta.
    """
    if shocks is None:
        shocks = [1.0, 2.0]

    base_emi = calculate_emi(principal, annual_rate, tenure_years)

    results = []
    for shock in shocks:
        shocked_rate = annual_rate + shock
        shocked_emi = calculate_emi(principal, shocked_rate, tenure_years)
        affordability = check_affordability(monthly_salary, shocked_emi["emi"], monthly_expenses)

        results.append({
            "shock_percent": shock,
            "original_rate": annual_rate,
            "shocked_rate": round(shocked_rate, 2),
            "original_emi": base_emi["emi"],
            "shocked_emi": shocked_emi["emi"],
            "emi_increase": round(shocked_emi["emi"] - base_emi["emi"], 2),
            "risk_level": affordability["risk_level"],
            "color": affordability["color"],
            "disposable_income": affordability.get("disposable_income", 0),
        })

    return results
