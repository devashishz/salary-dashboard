# 💸 Indian Salary & Tax Breakdown Dashboard

[![CI Pipeline](https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPO_NAME>/actions/workflows/ci.yml/badge.svg)](https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPO_NAME>/actions)
![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B.svg)
![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)

An interactive, institutional-grade salary engine and visualizer built with **Streamlit** and **Pandas**. This dashboard bridges the gap between **Cost to Company (CTC)**, **Taxable Gross**, and **Actual In-Hand Bank Credit** under the **New Tax Regime**.

---

## 📌 Problem Statement

In India, an offered CTC rarely represents the take-home cash credited to your bank account. Deductions such as **Employer PF**, **Gratuity provisions**, **NPS allocations**, **variable payout schedules**, and **TDS** make estimating net income complex.

This tool demystifies CTC structures by calculating:
- **True Gross Salary vs. CTC**
- **Retirement & Deferred Retirals:** EPF (Employee & Employer), Employer NPS under Section 80CCD(2), and Gratuity reserves
- **New Tax Regime Engine:** Slabs (0% to 30%), Section 87A rebate & marginal relief, surcharge threshold relief (>₹50L), and 4% Health & Education Cess
- **Cash Flow Timelines:** Separation of regular month take-home vs. bonus tranche payout months
- **Total Wealth Accrual:** Total realized economic value retained across cash and retirement assets

---

## ✨ Key Features

### 🎛️ 1. Flexible Input Engine
- **Fixed & Variable Compensation:** Model base salary packages and performance bonuses independently.
- **Payout Frequency Schedules:** Toggle variable pay distribution across **Annual Lump Sum (1x)**, **Semi-Annual (2x)**, **Quarterly (4x)**, or **Monthly (12x)**.
- **Configurable Retiral Structure:** Adjust Basic Salary percentage (30%–60%), toggle PF capping (Full 12% vs. statutory ₹1,800/month), and configure CTC gratuity absorption.
- **Employer NPS Optimization (Sec 80CCD(2)):** Toggle 14% Basic salary allocation to corporate NPS to analyze tax savings and take-home trade-offs.

### 📑 2. Detailed Multi-Tab Analysis
- **🏛️ Waterfall Payslip Breakdown:** A 5-stage lifecycle breakdown from Gross CTC $\rightarrow$ Employer Retirals $\rightarrow$ Taxable Gross $\rightarrow$ Employee Deductions $\rightarrow$ Net Bank Credit.
- **🧮 Tax Slab Audit & Surcharges:** Full visibility into how every income tranche is taxed across all slabs, including Standard Deduction (₹75,000), Section 87A relief, surcharge marginal relief, and cess.
- **💰 Total Wealth & Asset Accrual:** Complete asset allocation view showing where every rupee of your CTC goes (Liquid Cash, EPFO, NPS Tier-1, Gratuity Trust, and Government Taxes).

### 📈 3. Executive Metrics
- Real-time metric cards for **Total CTC**, **Regular Monthly In-Hand**, **Bonus Month In-Hand**, **Total Annual In-Hand**, and **Total Tax (TDS)**.

---

## 🏗️ Salary Flow Architecture

```text
Fixed CTC + Variable CTC
   │
   ├── (–) Employer Retirals (Employer PF + Gratuity + Employer NPS)
   │
   ▼
Taxable Gross Salary
   │
   ├── (–) Standard Deduction (₹75,000)
   ├── (–) Section 87A Rebate / Marginal Relief
   ├── (+) Surcharge (if > ₹50L) + Marginal Relief
   ├── (+) 4% Health & Education Cess
   │
   ▼
Total Tax (TDS) & Statutory Outflows (Employee PF + PT)
   │
   ▼
Net Realized In-Hand Bank Credit (Regular Month vs. Payout Months)