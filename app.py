"""
AI Finance Copilot — Streamlit UI (v2: XAI, Stress Test, Budget-Aware, Enhanced Scenarios)
"""

import streamlit as st
import pandas as pd

from agent import run_agent

# ───────────────────────── Page Config ─────────────────────────
st.set_page_config(
    page_title="AI Finance Copilot",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ───────────────────────── Custom CSS ─────────────────────────
st.markdown("""
<style>
    /* ---------- Global ---------- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* ---------- Header ---------- */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        color: white;
    }
    .main-header h1 { margin: 0; font-size: 2rem; font-weight: 700; }
    .main-header p  { margin: 0.4rem 0 0; opacity: 0.9; font-size: 1rem; }

    /* ---------- Metric cards ---------- */
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 14px;
        padding: 1.4rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        transition: transform 0.2s;
    }
    .metric-card:hover { transform: translateY(-3px); }
    .metric-card .label { font-size: 0.85rem; color: #555; font-weight: 500; }
    .metric-card .value { font-size: 1.6rem; font-weight: 700; color: #1a1a2e; margin-top: 0.3rem; }

    /* ---------- Risk badges ---------- */
    .badge       { display: inline-block; padding: 0.4rem 1.2rem; border-radius: 30px;
                   font-weight: 600; font-size: 0.95rem; letter-spacing: 0.3px; }
    .badge-safe  { background: #d4edda; color: #155724; }
    .badge-mod   { background: #fff3cd; color: #856404; }
    .badge-risky { background: #f8d7da; color: #721c24; }

    /* ---------- Explanation box ---------- */
    .explanation-box {
        background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
        border-radius: 14px;
        padding: 1.5rem 2rem;
        margin-top: 1.5rem;
        color: #1a1a2e;
        line-height: 1.7;
    }

    /* ---------- XAI panel ---------- */
    .xai-panel {
        background: linear-gradient(135deg, #fdfcfb 0%, #e2d1c3 100%);
        border-radius: 14px;
        padding: 1.5rem 2rem;
        margin-top: 1rem;
        border-left: 4px solid #e67e22;
    }
    .xai-panel h4 { margin: 0 0 0.8rem; color: #e67e22; }

    /* ---------- Stress test card ---------- */
    .stress-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border-radius: 14px;
        padding: 1.2rem 1.8rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    }
    .stress-card .shock-label { font-weight: 600; color: #c0392b; }

    /* ---------- Recommended badge ---------- */
    .rec-badge {
        display: inline-block;
        background: linear-gradient(135deg, #a8e063 0%, #56ab2f 100%);
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    /* ---------- Disclaimer ---------- */
    .disclaimer {
        margin-top: 2rem;
        padding: 1rem 1.5rem;
        background: #fff8e1;
        border-left: 4px solid #ffc107;
        border-radius: 8px;
        font-size: 0.85rem;
        color: #6d4c00;
    }

    /* ---------- Sidebar touches ---------- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    [data-testid="stSidebar"] * { color: #e0e0e0 !important; }
    [data-testid="stSidebar"] .stSlider label { font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# ───────────────────────── Header ─────────────────────────
st.markdown("""
<div class="main-header">
    <h1>💰 AI Finance Copilot</h1>
    <p>Agentic AI-powered loan planning &amp; affordability analysis — with explainability &amp; stress testing</p>
</div>
""", unsafe_allow_html=True)

# ───────────────────────── Sidebar ─────────────────────────
with st.sidebar:
    st.markdown("## 📋 Your Details")

    salary = st.number_input(
        "Monthly Salary (₹)",
        min_value=1000,
        max_value=10_000_000,
        value=50_000,
        step=5_000,
        help="Your monthly take-home salary",
    )

    monthly_expenses = st.number_input(
        "Monthly Expenses (₹)",
        min_value=0,
        max_value=10_000_000,
        value=15_000,
        step=1_000,
        help="Fixed expenses: rent, food, utilities, existing EMIs",
    )

    st.markdown("---")
    st.markdown("## 🏦 Loan Details")

    loan_amount = st.number_input(
        "Loan Amount (₹)",
        min_value=10_000,
        max_value=100_000_000,
        value=10_00_000,
        step=50_000,
        help="Total loan principal",
    )

    interest_rate = st.slider(
        "Interest Rate (% p.a.)",
        min_value=1.0,
        max_value=25.0,
        value=11.0,
        step=0.25,
    )

    tenure_years = st.slider(
        "Tenure (years)",
        min_value=1,
        max_value=30,
        value=5,
        step=1,
    )

    st.markdown("---")
    st.markdown("## ⚡ Advanced")

    enable_stress_test = st.checkbox("Enable Stress Test (+1%, +2% rate shock)", value=True)

    st.markdown("---")
    analyze_btn = st.button("🚀 Analyze My Loan", use_container_width=True, type="primary")

# ───────────────────────── Chat input ─────────────────────────
st.markdown("### 💬 Ask a question (optional)")
user_query = st.text_input(
    "e.g. 'Can I afford this loan?' or 'What if interest rates go up?'",
    label_visibility="collapsed",
    placeholder="e.g. Can I afford a 10L loan at 11% for 5 years with my expenses?",
)

# ───────────────────────── Main Logic ─────────────────────────
if analyze_btn:
    with st.spinner("🤖 Agent is analyzing your loan…"):
        result = run_agent(
            user_query=user_query,
            salary=salary,
            loan_amount=loan_amount,
            interest_rate=interest_rate,
            tenure_years=tenure_years,
            monthly_expenses=monthly_expenses,
            run_stress_test=enable_stress_test,
        )

    if not result["success"]:
        st.error(f"❌ {result['error']}")
    else:
        emi_data = result["emi"]
        aff_data = result["affordability"]
        scenarios = result["scenarios"]

        # ═══════════════════════ METRIC CARDS ═══════════════════════
        st.markdown("### 📊 Your Loan Summary")
        c1, c2, c3, c4, c5 = st.columns(5)

        with c1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Monthly EMI</div>
                <div class="value">₹{emi_data['emi']:,.0f}</div>
            </div>""", unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Total Interest</div>
                <div class="value">₹{emi_data['total_interest']:,.0f}</div>
            </div>""", unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Total Payment</div>
                <div class="value">₹{emi_data['total_payment']:,.0f}</div>
            </div>""", unsafe_allow_html=True)

        with c4:
            disp = aff_data["disposable_income"]
            disp_color = "#155724" if disp > 0 else "#721c24"
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Disposable Income</div>
                <div class="value" style="color:{disp_color}">₹{disp:,.0f}</div>
            </div>""", unsafe_allow_html=True)

        with c5:
            badge_class = {
                "Safe": "badge-safe",
                "Moderate": "badge-mod",
                "Risky": "badge-risky",
            }.get(aff_data["risk_level"], "badge-mod")
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Risk Level</div>
                <div class="value"><span class="badge {badge_class}">{aff_data['color']} {aff_data['risk_level']}</span></div>
            </div>""", unsafe_allow_html=True)

        # ═══════════════════ AFFORDABILITY DETAIL ═══════════════════
        st.markdown("---")
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(
                f"**EMI-to-Salary Ratio:** {aff_data['emi_to_salary_ratio']}% "
                f"(₹{emi_data['emi']:,.0f} / ₹{salary:,.0f})"
            )
        with col_b:
            st.markdown(
                f"**Disposable %:** {aff_data['disposable_percent']}% "
                f"(₹{aff_data['disposable_income']:,.0f} left after expenses + EMI)"
            )

        # ═══════════════════ XAI PANEL ═══════════════════
        st.markdown("### 🔍 Explainable AI (XAI) — Why This Rating?")
        xai = aff_data["xai"]

        with st.expander("View decision rules, thresholds & income breakdown", expanded=True):
            xai_col1, xai_col2 = st.columns(2)

            with xai_col1:
                st.markdown("**Decision Rules:**")
                for rule in xai["rules_applied"]:
                    st.markdown(f"- ✓ {rule}")
                st.markdown(f"\n**Decisive Factor:** `{xai['decisive_factor']}`")

            with xai_col2:
                bd = xai["income_breakdown"]
                st.markdown("**Income Breakdown:**")

                breakdown_df = pd.DataFrame({
                    "Item": ["💰 Salary", "📦 Expenses", "🏦 EMI", "💵 Disposable"],
                    "Amount (₹)": [
                        f"₹{bd['gross_salary']:,.0f}",
                        f"−₹{bd['fixed_expenses']:,.0f}",
                        f"−₹{bd['emi']:,.0f}",
                        f"₹{bd['disposable_income']:,.0f}",
                    ],
                    "% of Salary": [
                        "100%",
                        f"{(bd['fixed_expenses']/bd['gross_salary']*100):.1f}%",
                        f"{(bd['emi']/bd['gross_salary']*100):.1f}%",
                        f"{bd['disposable_percent']:.1f}%",
                    ]
                })
                st.dataframe(breakdown_df, hide_index=True, use_container_width=True)

        # ═══════════════ SCENARIO COMPARISON TABLE ═══════════════
        st.markdown("### 📈 Tenure Comparison")

        df = pd.DataFrame(scenarios)
        display_df = pd.DataFrame({
            "Tenure (yrs)": df["tenure_years"],
            "Monthly EMI (₹)": df["emi"].apply(lambda x: f"₹{x:,.0f}"),
            "Total Interest (₹)": df["total_interest"].apply(lambda x: f"₹{x:,.0f}"),
            "Total Payment (₹)": df["total_payment"].apply(lambda x: f"₹{x:,.0f}"),
            "Risk": df.apply(lambda r: f"{r['color']} {r['risk_level']}", axis=1),
            "": df["recommended"].apply(lambda r: "⭐ Recommended" if r else ""),
        })
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        # ═══════════════ STRESS TEST ═══════════════
        if result.get("stress_test"):
            st.markdown("### ⚡ Stress Test — What If Rates Rise?")

            stress_cols = st.columns(len(result["stress_test"]))
            for i, sr in enumerate(result["stress_test"]):
                with stress_cols[i]:
                    risk_badge = {
                        "Safe": "badge-safe",
                        "Moderate": "badge-mod",
                        "Risky": "badge-risky",
                    }.get(sr["risk_level"], "badge-mod")

                    st.markdown(f"""
                    <div class="stress-card">
                        <div class="shock-label">+{sr['shock_percent']}% Rate Shock</div>
                        <p style="margin:0.5rem 0 0.2rem; font-size:0.9rem;">
                            Rate: <b>{sr['original_rate']}% → {sr['shocked_rate']}%</b>
                        </p>
                        <p style="margin:0; font-size:0.9rem;">
                            EMI: <b>₹{sr['original_emi']:,.0f} → ₹{sr['shocked_emi']:,.0f}</b>
                            <span style="color:#c0392b; font-weight:600;"> (+₹{sr['emi_increase']:,.0f}/mo)</span>
                        </p>
                        <p style="margin:0.5rem 0 0;">
                            <span class="badge {risk_badge}">{sr['color']} {sr['risk_level']}</span>
                        </p>
                    </div>""", unsafe_allow_html=True)

        # ═══════════════ AI EXPLANATION ═══════════════
        st.markdown("### 🧠 AI Explanation")
        st.markdown(
            f'<div class="explanation-box">{result["explanation"]}</div>',
            unsafe_allow_html=True,
        )

# ───────────────────────── Disclaimer ─────────────────────────
st.markdown("""
<div class="disclaimer">
    ⚠️ <strong>Disclaimer:</strong> This is an educational decision-support tool, not professional
    financial advice. Please consult a certified financial advisor for personalized guidance.
</div>
""", unsafe_allow_html=True)
