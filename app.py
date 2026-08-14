import streamlit as st
import pandas as pd

# --- TAX CALCULATION LOGIC (NEW REGIME) ---
def calc_tax_new_regime(taxable_income):
    # Tax rebate up to 12L
    if taxable_income <= 1200000:
        return 0
    
    # Calculate slab wise
    tax = 0
    rem = taxable_income
    
    if rem > 2400000:
        tax += (rem - 2400000) * 0.30
        rem = 2400000
    if rem > 2000000:
        tax += (rem - 2000000) * 0.25
        rem = 2000000
    if rem > 1600000:
        tax += (rem - 1600000) * 0.20
        rem = 1600000
    if rem > 1200000:
        tax += (rem - 1200000) * 0.15
        rem = 1200000
    if rem > 800000:
        tax += (rem - 800000) * 0.10
        rem = 800000
    if rem > 400000:
        tax += (rem - 400000) * 0.05
    
    base_tax = tax
    
    # Surcharge & Marginal Relief for > 50L Income
    if taxable_income > 5000000:
        raw_surcharge = base_tax * 0.10
        excess_income = taxable_income - 5000000
        
        # Calculate base tax exactly at 50L threshold
        tax_at_50L = (5000000 - 2400000)*0.30 + 40000*0.25 + 40000*0.20 + 40000*0.15 + 40000*0.10 + 40000*0.05
        max_tax_allowed = tax_at_50L + excess_income
        
        if (base_tax + raw_surcharge) > max_tax_allowed:
            total_tax_before_cess = max_tax_allowed
        else:
            total_tax_before_cess = base_tax + raw_surcharge
    else:
        total_tax_before_cess = base_tax

    return total_tax_before_cess * 1.04 # 4% Health & Education Cess

# --- STREAMLIT UI & DASHBOARD ---
st.set_page_config(page_title="Indian Salary Dashboard", layout="wide", page_icon="💸")

st.title("💸 Indian Salary & Tax Dashboard")
st.markdown("Calculate your exact monthly in-hand salary based on your Fixed and Variable CTC under the **New Tax Regime**.")

# --- SIDEBAR INPUTS ---
st.sidebar.header("1. Enter Package Details")
fixed_ctc = st.sidebar.number_input("Fixed CTC (₹)", min_value=0, value=4100000, step=100000)
variable_ctc = st.sidebar.number_input("Variable CTC / Bonus (₹)", min_value=0, value=400000, step=50000)

st.sidebar.header("2. Salary Structure Assumptions")
basic_percent = st.sidebar.slider("Basic Salary % (of Fixed)", min_value=30, max_value=60, value=40, step=5)
pf_type = st.sidebar.radio("Provident Fund (PF) Deduction", ["Full (12% of Basic)", "Capped (₹1,800/mo)"])
include_gratuity = st.sidebar.checkbox("Is Gratuity deducted from Fixed CTC?", value=True)

# --- CALCULATIONS ---
# 1. Base Components
basic = fixed_ctc * (basic_percent / 100.0)

if pf_type == "Full (12% of Basic)":
    employer_pf = basic * 0.12
    employee_pf = basic * 0.12
else:
    employer_pf = 1800 * 12
    employee_pf = 1800 * 12

gratuity = (basic * 0.0481) if include_gratuity else 0

# 2. Gross Salary Calculation
fixed_gross = fixed_ctc - employer_pf - gratuity
total_gross = fixed_gross + variable_ctc

# 3. Tax Calculation
standard_deduction = 75000
taxable_income = max(0, total_gross - standard_deduction)
total_tax = calc_tax_new_regime(taxable_income)

pt_annual = 2400

# 4. In-Hand Calculation
total_deductions = employee_pf + total_tax + pt_annual
annual_in_hand = total_gross - total_deductions

# --- METRICS DISPLAY ---
st.write("### 📈 Quick Summary")
col1, col2, col3, col4 = st.columns(4)

monthly_fixed_in_hand = (fixed_gross - employee_pf - total_tax - pt_annual) / 12

col1.metric("Total CTC (Fixed + Var)", f"₹{(fixed_ctc + variable_ctc):,.0f}")
col2.metric("Base Monthly In-Hand", f"₹{monthly_fixed_in_hand:,.0f}", help="Monthly take-home strictly from Fixed CTC (assuming tax is divided equally over 12 months)")
col3.metric("Annual In-Hand", f"₹{annual_in_hand:,.0f}", help="Total cash you take home in a year (including Variable payouts)")
col4.metric("Total Income Tax", f"₹{total_tax:,.0f}")

st.divider()

# --- SUMMARY COMPARISON TABLE ---
st.write("### 📊 Detailed Breakdown")

# Creating a DataFrame to display the structured summary
breakdown_data = {
    "Component": [
        "Base Salary (Basic)",
        "Employer PF",
        "Gratuity Reserve",
        "Gross Salary (Pre-Tax)",
        "Employee PF",
        "Professional Tax",
        "Income Tax (TDS)",
        "Net In-Hand"
    ],
    "Fixed (Annual)": [
        f"₹{basic:,.0f}",
        f"- ₹{employer_pf:,.0f}",
        f"- ₹{gratuity:,.0f}",
        f"₹{fixed_gross:,.0f}",
        f"- ₹{employee_pf:,.0f}",
        f"- ₹{pt_annual:,.0f}",
        f"₹{total_tax:,.0f} (Total)", # Displaying total tax logic
        f"₹{(fixed_gross - employee_pf - pt_annual - total_tax):,.0f}"
    ],
    "Variable (Annual)": [
        "₹0",
        "₹0",
        "₹0",
        f"₹{variable_ctc:,.0f}",
        "₹0",
        "₹0",
        "-",
        f"₹{variable_ctc:,.0f}" # Simplified mapping (Taxes applied globally)
    ],
    "Total Annual": [
        f"₹{basic:,.0f}",
        f"₹{employer_pf:,.0f}",
        f"₹{gratuity:,.0f}",
        f"₹{total_gross:,.0f}",
        f"₹{employee_pf:,.0f}",
        f"₹{pt_annual:,.0f}",
        f"₹{total_tax:,.0f}",
        f"₹{annual_in_hand:,.0f}"
    ],
    "Average Monthly": [
        f"₹{(basic/12):,.0f}",
        f"₹{(employer_pf/12):,.0f}",
        f"₹{(gratuity/12):,.0f}",
        f"₹{(total_gross/12):,.0f}",
        f"₹{(employee_pf/12):,.0f}",
        f"₹{(pt_annual/12):,.0f}",
        f"₹{(total_tax/12):,.0f}",
        f"₹{(annual_in_hand/12):,.0f}"
    ]
}

df_breakdown = pd.DataFrame(breakdown_data)

# Displaying table without the default index
st.dataframe(df_breakdown, use_container_width=True, hide_index=True)

st.caption("*Note: The monthly average assumes the variable bonus is spread equally across 12 months. In reality, variable pay is usually paid out as a lump sum once or twice a year, meaning your standard monthly paycheck will reflect the 'Base Monthly In-Hand' figure above, with a large spike in your bonus month.*")