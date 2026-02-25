# 💰 AI Finance Copilot — Agentic GenAI App

An AI-powered financial planning assistant built with **Streamlit** and **Groq LLM**. Uses a tool-calling agentic architecture for EMI simulation, budget-aware affordability risk analysis, stress testing, and scenario-based decision support — with full explainability.

> ⚠️ This is an educational decision-support tool, not professional financial advice.

---

## 🎯 Problem Statement

Taking a loan is one of the most important financial decisions. Yet most people rely on rough mental math or opaque bank calculators. This app provides:

- **Accurate EMI calculations** (deterministic, no hallucination)
- **Budget-aware affordability** (considers expenses, not just salary)
- **Stress testing** (simulates +1% / +2% rate shocks)
- **Explainable AI** (transparent decision rules and thresholds)
- **Scenario comparison** with recommended option
- **AI-powered explanations** in plain language

---

## 🏗️ Agentic Architecture

```
User Input (Salary, Expenses, Loan, Rate, Tenure)
        │
        ▼
   ┌─────────┐
   │  Agent   │  ← Parses intent, routes to tools
   └────┬─────┘
        │
   ┌────┼──────────────────────────┐
   ▼    ▼            ▼             ▼
EMI   Budget-Aware  Scenario    Stress
Tool  Affordability Simulator   Tester
        │            │             │
   └────┼────────────┼─────────────┘
        │
        ▼
   ┌───────────────┐
   │ XAI Layer     │  ← Exposes rules, thresholds, breakdown
   └───────┬───────┘
           │
   ┌───────▼───────┐
   │   Groq LLM    │  ← Explains outputs (never computes)
   └───────────────┘
        │
        ▼
   Streamlit UI
```

### Why Tools + LLM Separation?

| Concern | Who handles it |
|---------|---------------|
| Math (EMI, ratios, disposable income) | **Deterministic Python tools** |
| Risk rules & thresholds | **Explainability (XAI) layer** |
| Natural language explanation | **Groq LLM** |

This prevents **hallucinated numbers** — the LLM only explains, never computes.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🔍 **XAI Panel** | Transparent decision rules, thresholds, income breakdown |
| ⚡ **Stress Test** | +1% / +2% interest rate shock simulation |
| 💰 **Budget-Aware** | Risk based on disposable income (salary − expenses − EMI) |
| 📈 **Smart Scenarios** | 3/5/7yr comparison with risk labels + ⭐ Recommended |
| 🧠 **AI Explanation** | Groq LLM explains trade-offs in plain language |

---

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone <your-repo-url>
cd ai-finance-copilot
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. Add API Key
Create a `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Run
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
ai-finance-copilot/
├── app.py                  # Streamlit UI (v2)
├── agent.py                # Agent routing logic
├── llm.py                  # Groq client wrapper
├── tools/
│   ├── emi.py              # EMI calculator
│   ├── affordability.py    # Budget-aware risk classifier + XAI
│   ├── simulator.py        # Tenure comparison + recommended
│   └── stress_test.py      # Interest rate shock simulator
├── prompts/
│   └── system_prompt.txt   # LLM system prompt
├── .env                    # API key (never commit)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **LLM**: Groq (Llama 3.3 70B)
- **Language**: Python 3.10+
- **Architecture**: Agentic (tool-calling pattern) with XAI layer

---

## 📦 Deployment (Streamlit Cloud)

1. Push to GitHub (`.env` is gitignored)
2. Go to [Streamlit Community Cloud](https://share.streamlit.io)
3. Connect your repo
4. Add `GROQ_API_KEY` in **Secrets Manager**

---

## 📄 License

MIT
