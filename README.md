# 💸 Indian Salary & Tax Breakdown Dashboard

An interactive, accurate financial calculator and salary visualizer built with **Streamlit** and **Python**. This dashboard bridges the gap between **Cost to Company (CTC)** and **Actual In-Hand Salary** in India under the **New Tax Regime**.

---

## 📌 Problem Statement

In India, an offered CTC (Cost to Company) rarely equals the monthly amount credited to an employee's bank account. Complex salary structures including **Employer PF**, **Gratuity provisions**, **variable payouts**, and **Income Tax (TDS)** make it difficult to estimate actual net take-home pay.

This tool demystifies CTC breakdowns by computing:
- Exact Gross Salary vs. CTC
- Mandatory employer & employee retirement deductions (PF & Gratuity)
- Slabs, rebates, and surcharges under the New Tax Regime
- Accurate monthly vs. annual take-home amounts

---

## ✨ Features

- **Interactive Inputs:** Customize Fixed CTC, Variable Pay/Bonus, and Basic Salary percentage.
- **Configurable PF Rules:** Toggle between full Provident Fund deduction (12% of basic) or statutory capped limit (₹1,800/month).
- **Gratuity Toggle:** Account for whether Gratuity is carved out of the Fixed CTC.
- **Accurate Tax Engine:** 
  - Standard Deduction of ₹75,000.
  - Full tax rebate under Section 87A for taxable incomes up to ₹12 Lakhs.
  - Multi-slab New Tax Regime rates (5% up to 30%).
  - 10% Surcharge on incomes > ₹50 Lakhs with **Marginal Relief** safeguard.
  - 4% Health & Education Cess.
- **Clean Visuals & Metrics:** High-level overview cards and a structured tabular comparison breakdown.