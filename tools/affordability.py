"""
Affordability Risk Analyzer — Budget-aware with XAI transparency. No LLM.
"""


# Decision thresholds (exposed for XAI)
THRESHOLDS = {
    "safe_max_ratio": 30,
    "moderate_max_ratio": 40,
    "min_disposable_percent": 20,
}


def check_affordability(
    monthly_salary: float,
    emi: float,
    monthly_expenses: float = 0,
) -> dict:
    """
    Assess loan affordability based on EMI-to-salary ratio AND post-expense cashflow.

    Args:
        monthly_salary: Monthly take-home salary.
        emi: Monthly EMI amount.
        monthly_expenses: Fixed monthly expenses (rent, food, existing EMIs).

    Returns:
        dict with ratio, risk_level, verdict, XAI breakdown, and color code.
    """
    if monthly_salary <= 0:
        raise ValueError("Monthly salary must be positive.")
    if emi < 0:
        raise ValueError("EMI cannot be negative.")
    if monthly_expenses < 0:
        raise ValueError("Monthly expenses cannot be negative.")

    # ── Core metrics ──
    emi_ratio = (emi / monthly_salary) * 100
    disposable_income = monthly_salary - monthly_expenses - emi
    disposable_percent = (disposable_income / monthly_salary) * 100 if monthly_salary > 0 else 0

    # ── Risk classification (budget-aware) ──
    # Risk is WORST of: ratio-based risk OR cashflow-based risk
    if emi_ratio <= THRESHOLDS["safe_max_ratio"] and disposable_percent >= THRESHOLDS["min_disposable_percent"]:
        risk_level = "Safe"
        verdict = (
            "Your EMI is well within the recommended limit and you retain healthy "
            "disposable income after all expenses."
        )
        color = "🟢"
    elif emi_ratio <= THRESHOLDS["moderate_max_ratio"] and disposable_percent >= 10:
        risk_level = "Moderate"
        verdict = (
            "Your EMI is approaching the upper limit. After expenses, your remaining "
            "cashflow is tight — consider building an emergency fund first."
        )
        color = "🟡"
    else:
        risk_level = "Risky"
        if disposable_income <= 0:
            verdict = (
                "After expenses and EMI, you would have negative or zero disposable income. "
                "This loan is not affordable at current income/expense levels."
            )
        else:
            verdict = (
                "Your EMI exceeds the safe threshold and/or leaves very little disposable income. "
                "This could strain your monthly budget significantly."
            )
        color = "🔴"

    # ── XAI explainability data ──
    xai = {
        "rules_applied": [
            f"EMI ≤ {THRESHOLDS['safe_max_ratio']}% of salary → Safe",
            f"EMI {THRESHOLDS['safe_max_ratio']}–{THRESHOLDS['moderate_max_ratio']}% of salary → Moderate",
            f"EMI > {THRESHOLDS['moderate_max_ratio']}% of salary → Risky",
            f"Disposable income < {THRESHOLDS['min_disposable_percent']}% of salary → escalates risk",
        ],
        "thresholds": THRESHOLDS,
        "income_breakdown": {
            "gross_salary": round(monthly_salary, 2),
            "fixed_expenses": round(monthly_expenses, 2),
            "emi": round(emi, 2),
            "disposable_income": round(disposable_income, 2),
            "disposable_percent": round(disposable_percent, 2),
        },
        "decisive_factor": (
            "cashflow" if (emi_ratio <= THRESHOLDS["moderate_max_ratio"] and disposable_percent < THRESHOLDS["min_disposable_percent"])
            else "emi_ratio"
        ),
    }

    return {
        "emi": round(emi, 2),
        "monthly_salary": round(monthly_salary, 2),
        "monthly_expenses": round(monthly_expenses, 2),
        "emi_to_salary_ratio": round(emi_ratio, 2),
        "disposable_income": round(disposable_income, 2),
        "disposable_percent": round(disposable_percent, 2),
        "risk_level": risk_level,
        "verdict": verdict,
        "color": color,
        "xai": xai,
    }
