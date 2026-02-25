"""
Scenario Simulator — Compare EMI across tenures with risk labels. No LLM.
"""

from tools.emi import calculate_emi
from tools.affordability import check_affordability


def simulate_scenarios(
    principal: float,
    annual_rate: float,
    monthly_salary: float,
    monthly_expenses: float = 0,
    tenures: list[int] | None = None,
) -> list[dict]:
    """
    Run EMI calculations across multiple tenure options with risk labels
    and a recommended flag.

    Args:
        principal: Loan amount.
        annual_rate: Annual interest rate (%).
        monthly_salary: Monthly take-home salary.
        monthly_expenses: Fixed monthly expenses.
        tenures: List of tenure values in years. Defaults to [3, 5, 7].

    Returns:
        List of dicts, one per tenure, with EMI details + risk + recommended flag.
    """
    if tenures is None:
        tenures = [3, 5, 7]

    scenarios = []
    for years in tenures:
        emi_result = calculate_emi(principal, annual_rate, years)
        affordability = check_affordability(monthly_salary, emi_result["emi"], monthly_expenses)

        scenarios.append({
            "tenure_years": years,
            "emi": emi_result["emi"],
            "total_interest": emi_result["total_interest"],
            "total_payment": emi_result["total_payment"],
            "risk_level": affordability["risk_level"],
            "color": affordability["color"],
            "disposable_income": affordability["disposable_income"],
            "recommended": False,  # set below
        })

    # ── Mark recommended: safest option with lowest total cost ──
    safe_scenarios = [s for s in scenarios if s["risk_level"] == "Safe"]
    if safe_scenarios:
        best = min(safe_scenarios, key=lambda s: s["total_payment"])
        best["recommended"] = True
    else:
        # No safe option — recommend the one with lowest risk + lowest cost
        moderate = [s for s in scenarios if s["risk_level"] == "Moderate"]
        if moderate:
            best = min(moderate, key=lambda s: s["total_payment"])
            best["recommended"] = True
        else:
            # All risky — recommend longest tenure (lowest EMI)
            longest = max(scenarios, key=lambda s: s["tenure_years"])
            longest["recommended"] = True

    return scenarios
