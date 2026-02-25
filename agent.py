"""
Agent Orchestration — Parses user intent, routes to tools, asks LLM to explain.
"""

import re

from tools.emi import calculate_emi
from tools.affordability import check_affordability
from tools.simulator import simulate_scenarios
from tools.stress_test import stress_test
from llm import get_llm_explanation


def _extract_numbers(text: str) -> list[float]:
    """Pull all numbers (int or float) from a string."""
    return [float(x) for x in re.findall(r"\d+\.?\d*", text)]


def _format_emi_result(result: dict) -> str:
    return (
        f"• Loan Amount: ₹{result['principal']:,.2f}\n"
        f"• Interest Rate: {result['annual_rate']}% p.a.\n"
        f"• Tenure: {result['tenure_months']} months\n"
        f"• Monthly EMI: ₹{result['emi']:,.2f}\n"
        f"• Total Interest: ₹{result['total_interest']:,.2f}\n"
        f"• Total Payment: ₹{result['total_payment']:,.2f}"
    )


def _format_affordability(result: dict) -> str:
    lines = [
        f"• Monthly Salary: ₹{result['monthly_salary']:,.2f}",
        f"• Fixed Expenses: ₹{result['monthly_expenses']:,.2f}",
        f"• Monthly EMI: ₹{result['emi']:,.2f}",
        f"• Disposable Income (after expenses + EMI): ₹{result['disposable_income']:,.2f}",
        f"• EMI-to-Salary Ratio: {result['emi_to_salary_ratio']}%",
        f"• Disposable Income %: {result['disposable_percent']}%",
        f"• Risk Level: {result['color']} {result['risk_level']}",
        f"• Verdict: {result['verdict']}",
    ]
    return "\n".join(lines)


def _format_xai(xai: dict) -> str:
    lines = ["Decision Rules Applied:"]
    for rule in xai["rules_applied"]:
        lines.append(f"  ✓ {rule}")
    bd = xai["income_breakdown"]
    lines.append(f"\nIncome Breakdown:")
    lines.append(f"  Salary: ₹{bd['gross_salary']:,.2f}")
    lines.append(f"  − Expenses: ₹{bd['fixed_expenses']:,.2f}")
    lines.append(f"  − EMI: ₹{bd['emi']:,.2f}")
    lines.append(f"  = Disposable: ₹{bd['disposable_income']:,.2f} ({bd['disposable_percent']}%)")
    lines.append(f"\nDecisive Factor: {xai['decisive_factor']}")
    return "\n".join(lines)


def _format_scenarios(scenarios: list[dict]) -> str:
    lines = ["Tenure Comparison:"]
    lines.append(f"{'Tenure':<10} {'EMI':>12} {'Total Interest':>16} {'Total Payment':>16} {'Risk':>10} {'Pick':>5}")
    lines.append("-" * 75)
    for s in scenarios:
        rec = "⭐" if s["recommended"] else ""
        lines.append(
            f"{s['tenure_years']} years{'':<4} "
            f"₹{s['emi']:>10,.2f} "
            f"₹{s['total_interest']:>14,.2f} "
            f"₹{s['total_payment']:>14,.2f} "
            f"{s['color']}{s['risk_level']:>8} "
            f"{rec}"
        )
    return "\n".join(lines)


def _format_stress_test(results: list[dict]) -> str:
    lines = ["Interest Rate Stress Test:"]
    for r in results:
        lines.append(
            f"  +{r['shock_percent']}% → Rate {r['shocked_rate']}% | "
            f"EMI ₹{r['shocked_emi']:,.2f} (+₹{r['emi_increase']:,.2f}/mo) | "
            f"Risk: {r['color']} {r['risk_level']}"
        )
    return "\n".join(lines)


def run_agent(
    user_query: str,
    salary: float,
    loan_amount: float,
    interest_rate: float,
    tenure_years: int,
    monthly_expenses: float = 0,
    run_stress_test: bool = True,
) -> dict:
    """
    Main agent entry point.

    1. Runs EMI tool
    2. Runs budget-aware affordability tool
    3. Runs scenario simulator (with risk labels + recommended)
    4. Optionally runs stress test
    5. Builds XAI explainability block
    6. Sends all results to LLM for explanation

    Returns dict with structured results + LLM explanation.
    """
    errors = []
    if salary <= 0:
        errors.append("Salary must be positive.")
    if loan_amount <= 0:
        errors.append("Loan amount must be positive.")
    if interest_rate < 0:
        errors.append("Interest rate cannot be negative.")
    if tenure_years <= 0:
        errors.append("Tenure must be at least 1 year.")
    if monthly_expenses < 0:
        errors.append("Expenses cannot be negative.")

    if errors:
        return {
            "success": False,
            "error": " ".join(errors),
        }

    # --- Tool calls (deterministic) ---
    emi_result = calculate_emi(loan_amount, interest_rate, tenure_years)
    affordability_result = check_affordability(salary, emi_result["emi"], monthly_expenses)
    scenario_results = simulate_scenarios(loan_amount, interest_rate, salary, monthly_expenses)

    stress_results = None
    if run_stress_test:
        stress_results = stress_test(
            loan_amount, interest_rate, tenure_years, salary, monthly_expenses
        )

    # --- Format tool outputs for LLM ---
    sections = [
        "=== EMI Calculation ===",
        _format_emi_result(emi_result),
        "=== Budget-Aware Affordability Assessment ===",
        _format_affordability(affordability_result),
        "=== Explainability (XAI) ===",
        _format_xai(affordability_result["xai"]),
        "=== Scenario Comparison ===",
        _format_scenarios(scenario_results),
    ]

    if stress_results:
        sections.append("=== Stress Test (Rate Shocks) ===")
        sections.append(_format_stress_test(stress_results))

    tool_output_text = "\n\n".join(sections)

    # --- LLM explanation ---
    if not user_query.strip():
        user_query = (
            f"I earn ₹{salary:,.0f}/month with ₹{monthly_expenses:,.0f} in fixed expenses. "
            f"I want a ₹{loan_amount:,.0f} loan at {interest_rate}% for {tenure_years} years. "
            f"Is it affordable? What happens if rates increase?"
        )

    explanation = get_llm_explanation(user_query, tool_output_text)

    return {
        "success": True,
        "emi": emi_result,
        "affordability": affordability_result,
        "scenarios": scenario_results,
        "stress_test": stress_results,
        "tool_output_text": tool_output_text,
        "explanation": explanation,
    }
