import pandas as pd
import streamlit as st

# Must be the first Streamlit command
st.set_page_config(page_title="Indian Salary Dashboard", layout="wide", page_icon="💸")

# --- TAX CALCULATION LOGIC (NEW REGIME) ---
def get_tax_breakdown(taxable_income):
    """Calculates tax and returns slab-wise breakdown dictionary."""
    slabs_config = [
        {"slab": "₹0 - ₹4,00,000", "min": 0, "max": 400000, "rate": 0.00},
        {"slab": "₹4,00,001 - ₹8,00,000", "min": 400000, "max": 800000, "rate": 0.05},
        {"slab": "₹8,00,001 - ₹12,00,000", "min": 800000, "max": 1200000, "rate": 0.10},
        {"slab": "₹12,00,001 - ₹16,00,000", "min": 1200000, "max": 1600000, "rate": 0.15},
        {"slab": "₹16,00,001 - ₹20,00,000", "min": 1600000, "max": 2000000, "rate": 0.20},
        {"slab": "₹20,00,001 - ₹24,00,000", "min": 2000000, "max": 2400000, "rate": 0.25},
        {"slab": "Above ₹24,00,000", "min": 2400000, "max": float("inf"), "rate": 0.30},
    ]
    rebate_limit_87a = 1200000
    surcharge_threshold = 5000000
    surcharge_rate = 0.10
    cess_rate = 0.04

    slab_records = []
    base_tax = 0.0

    for s in slabs_config:
        if taxable_income > s["min"]:
            taxable_in_slab = min(taxable_income, s["max"]) - s["min"]
            tax_in_slab = taxable_in_slab * s["rate"]
            base_tax += tax_in_slab
            slab_records.append({
                "Income Slab": s["slab"],
                "Tax Rate": f"{int(s['rate']*100)}%",
                "Taxable Amount in Slab": taxable_in_slab,
                "Tax Calculated": tax_in_slab
            })
        else:
            slab_records.append({
                "Income Slab": s["slab"],
                "Tax Rate": f"{int(s['rate']*100)}%",
                "Taxable Amount in Slab": 0.0,
                "Tax Calculated": 0.0
            })

    # Section 87A Rebate & Marginal Relief
    rebate_87a = 0.0
    if taxable_income <= rebate_limit_87a:
        rebate_87a = base_tax
        base_tax = 0.0
    else:
        excess_over_12l = taxable_income - rebate_limit_87a
        if base_tax > excess_over_12l:
            rebate_87a = base_tax - excess_over_12l
            base_tax = excess_over_12l

    # Surcharge Calculation
    surcharge = 0.0
    total_tax_before_cess = base_tax
    if taxable_income > surcharge_threshold:
        raw_surcharge = base_tax * surcharge_rate
        tax_at_50L = 1080000.0
        excess_over_50l = taxable_income - surcharge_threshold
        max_tax_allowed = tax_at_50L + excess_over_50l
        if (base_tax + raw_surcharge) > max_tax_allowed:
            surcharge = max(0.0, max_tax_allowed - base_tax)
            total_tax_before_cess = max_tax_allowed
        else:
            surcharge = raw_surcharge
            total_tax_before_cess = base_tax + raw_surcharge

    cess = total_tax_before_cess * cess_rate
    total_tax = total_tax_before_cess + cess

    return {
        "slab_records": slab_records,
        "base_tax": base_tax,
        "rebate_87a": rebate_87a,
        "surcharge": surcharge,
        "cess": cess,
        "total_tax": total_tax
    }

# --- STREAMLIT UI & DASHBOARD ---
st.title("💸 Indian Salary & Tax Dashboard")
st.markdown("A structured financial engine to calculate your take-home pay, tax liability, and wealth accrual under the **New Tax Regime**.")

# --- SIDEBAR INPUTS ---
st.sidebar.header("1. Enter Package Details")
fixed_ctc = st.sidebar.number_input("Fixed CTC (₹)", min_value=0, value=4100000, step=100000)
variable_ctc = st.sidebar.number_input("Variable CTC / Bonus (₹)", min_value=0, value=400000, step=50000)

st.sidebar.header("2. Payout Structure")
variable_payout_mode = st.sidebar.radio(
    "Variable Pay Frequency",
    ["Annual Lump Sum (1x / year)", "Semi-Annual (2x / year)", "Quarterly (4x / year)", "Monthly (Spread across 12 months)"],
    index=0
)

st.sidebar.header("3. Structure & Retirals")
basic_percent = st.sidebar.slider("Basic Salary % (of Fixed)", min_value=30, max_value=60, value=40, step=5)
pf_type = st.sidebar.radio("Provident Fund (PF) Deduction", ["Full (12% of Basic)", "Capped (₹1,800/mo)"])
include_gratuity = st.sidebar.checkbox("Is Gratuity deducted from Fixed CTC?", value=True)

st.sidebar.header("4. Tax Optimizations")
enable_nps = st.sidebar.toggle(
    "Opt-in Employer NPS (14% of Basic)",
    value=False,
    help="Under Section 80CCD(2), Employer contribution up to 14% of Basic Salary is tax-free in the New Tax Regime."
)

# --- ENGINE CALCULATIONS ---
basic = fixed_ctc * (basic_percent / 100.0)

if pf_type == "Full (12% of Basic)":
    employer_pf = basic * 0.12
    employee_pf = basic * 0.12
else:
    employer_pf = 1800 * 12
    employee_pf = 1800 * 12

employer_nps = (basic * 0.14) if enable_nps else 0.0
gratuity = (basic * 0.0481) if include_gratuity else 0.0

fixed_gross = fixed_ctc - employer_pf - employer_nps - gratuity
total_gross = fixed_gross + variable_ctc

standard_deduction = 75000.0
taxable_income_total = max(0.0, total_gross - standard_deduction)
tax_details_total = get_tax_breakdown(taxable_income_total)
total_tax = tax_details_total["total_tax"]

taxable_fixed = max(0.0, fixed_gross - standard_deduction)
tax_details_fixed = get_tax_breakdown(taxable_fixed)
fixed_tax = tax_details_fixed["total_tax"]
variable_tax = max(0.0, total_tax - fixed_tax)

pt_annual = 2400.0

annual_fixed_in_hand = fixed_gross - employee_pf - fixed_tax - pt_annual
annual_variable_in_hand = variable_ctc - variable_tax
annual_total_in_hand = annual_fixed_in_hand + annual_variable_in_hand
regular_monthly_in_hand = annual_fixed_in_hand / 12

if variable_payout_mode == "Monthly (Spread across 12 months)":
    payout_count = 12
    bonus_per_payout = annual_variable_in_hand / 12
elif variable_payout_mode == "Quarterly (4x / year)":
    payout_count = 4
    bonus_per_payout = annual_variable_in_hand / 4
elif variable_payout_mode == "Semi-Annual (2x / year)":
    payout_count = 2
    bonus_per_payout = annual_variable_in_hand / 2
else:
    payout_count = 1
    bonus_per_payout = annual_variable_in_hand

bonus_month_in_hand = regular_monthly_in_hand + bonus_per_payout

# --- TOP LEVEL METRICS ---
st.write("### 📈 Executive Summary")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total CTC", f"₹{(fixed_ctc + variable_ctc):,.0f}")
col2.metric("Regular In-Hand / mo", f"₹{regular_monthly_in_hand:,.0f}", help="Fixed take-home cash in non-bonus months")
col3.metric("Bonus Month In-Hand", f"₹{bonus_month_in_hand:,.0f}", help=f"Regular monthly pay + net bonus tranche (₹{bonus_per_payout:,.0f})")
col4.metric("Total Annual In-Hand", f"₹{annual_total_in_hand:,.0f}", help="Total take-home cash across all 12 months")
col5.metric("Total Tax (TDS)", f"₹{total_tax:,.0f}", help="Total income tax deducted across full income")

st.divider()

# --- ENHANCED TABBED BREAKDOWN ---
st.write("### 📑 Deep-Dive Breakdown & Analysis")
tab1, tab2, tab3 = st.tabs(["🏛️ Waterfall Payslip Breakdown", "🧮 Tax Slab Audit & Surcharges", "💰 Total Wealth & Asset Accrual"])

with tab1:
    st.markdown("#### **Stage-by-Stage Salary Waterfall**")
    
    waterfall_rows = [
        {"Category": "1. Gross CTC", "Component": "Fixed Base CTC", "Annual": f"₹{fixed_ctc:,.0f}", "Monthly": f"₹{(fixed_ctc/12):,.0f}", "Notes": "Total agreed fixed package"},
        {"Category": "1. Gross CTC", "Component": "Variable CTC / Bonus", "Annual": f"₹{variable_ctc:,.0f}", "Monthly": f"₹{(variable_ctc/12):,.0f}", "Notes": "Performance incentive"},
        
        {"Category": "2. Employer Retirals (Carved from CTC)", "Component": "Employer Provident Fund (PF)", "Annual": f"- ₹{employer_pf:,.0f}", "Monthly": f"- ₹{(employer_pf/12):,.0f}", "Notes": "12% of Basic credited to EPF"},
        {"Category": "2. Employer Retirals (Carved from CTC)", "Component": "Employer NPS (Sec 80CCD(2))", "Annual": f"- ₹{employer_nps:,.0f}", "Monthly": f"- ₹{(employer_nps/12):,.0f}", "Notes": "Tax-exempt corporate NPS investment"},
        {"Category": "2. Employer Retirals (Carved from CTC)", "Component": "Gratuity Provision", "Annual": f"- ₹{gratuity:,.0f}", "Monthly": f"- ₹{(gratuity/12):,.0f}", "Notes": "Retained by company, payable at exit"},
        
        {"Category": "3. Gross Earnings", "Component": "Taxable Gross Salary", "Annual": f"₹{total_gross:,.0f}", "Monthly": f"₹{(total_gross/12):,.0f}", "Notes": "Base amount on monthly payslip"},
        
        {"Category": "4. Employee Deductions", "Component": "Employee Provident Fund (EPF)", "Annual": f"- ₹{employee_pf:,.0f}", "Monthly": f"- ₹{(employee_pf/12):,.0f}", "Notes": "Your monthly contribution to EPF"},
        {"Category": "4. Employee Deductions", "Component": "Professional Tax (PT)", "Annual": f"- ₹{pt_annual:,.0f}", "Monthly": f"- ₹{(pt_annual/12):,.0f}", "Notes": "State statutory tax (₹200/mo)"},
        {"Category": "4. Employee Deductions", "Component": "Income Tax (TDS on Total)", "Annual": f"- ₹{total_tax:,.0f}", "Monthly": f"- ₹{(total_tax/12):,.0f}", "Notes": "Computed under New Tax Regime"},
        
        {"Category": "5. Net In-Hand Cash", "Component": "Regular Monthly Bank Credit", "Annual": f"₹{annual_fixed_in_hand:,.0f}", "Monthly": f"₹{regular_monthly_in_hand:,.0f}", "Notes": "Actual cash credited in standard months"},
        {"Category": "5. Net In-Hand Cash", "Component": "Total Net In-Hand (w/ Bonus)", "Annual": f"₹{annual_total_in_hand:,.0f}", "Monthly": f"₹{(annual_total_in_hand/12):,.0f}", "Notes": "Total net cash received across the year"},
    ]
    
    df_waterfall = pd.DataFrame(waterfall_rows)
    st.dataframe(df_waterfall, use_container_width=True, hide_index=True)
    
    if variable_payout_mode == "Monthly (Spread across 12 months)":
        st.caption("💡 **Payout Schedule:** Your variable bonus is distributed evenly every month (₹" + f"{bonus_per_payout:,.0f}" + "/mo net).")
    else:
        st.caption(f"💡 **Payout Schedule:** You will receive **₹{regular_monthly_in_hand:,.0f}** for **{12 - payout_count} regular months** and **₹{bonus_month_in_hand:,.0f}** during **{payout_count} bonus month(s)**.")

with tab2:
    st.markdown("#### **Tax Slabs & Calculation Audit (New Regime)**")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Gross Taxable Income", f"₹{total_gross:,.0f}")
    c2.metric("Standard Deduction", f"₹{standard_deduction:,.0f}")
    c3.metric("Net Taxable Income", f"₹{taxable_income_total:,.0f}")
    
    # Slab Table
    df_slabs = pd.DataFrame(tax_details_total["slab_records"])
    df_slabs["Taxable Amount in Slab"] = df_slabs["Taxable Amount in Slab"].apply(lambda x: f"₹{x:,.0f}")
    df_slabs["Tax Calculated"] = df_slabs["Tax Calculated"].apply(lambda x: f"₹{x:,.0f}")
    st.dataframe(df_slabs, use_container_width=True, hide_index=True)
    
    # Tax components breakdown
    st.markdown("**Tax Adjustments & Summary:**")
    summary_tax_rows = [
        {"Tax Item": "Base Slab Tax", "Amount": f"₹{tax_details_total['base_tax']:,.0f}"},
        {"Tax Item": "Section 87A Rebate / Marginal Relief", "Amount": f"- ₹{tax_details_total['rebate_87a']:,.0f}"},
        {"Tax Item": "Surcharge (Income > ₹50L)", "Amount": f"+ ₹{tax_details_total['surcharge']:,.0f}"},
        {"Tax Item": "Health & Education Cess (4%)", "Amount": f"+ ₹{tax_details_total['cess']:,.0f}"},
        {"Tax Item": "Total Final Tax Payable", "Amount": f"₹{total_tax:,.0f}"},
    ]
    st.dataframe(pd.DataFrame(summary_tax_rows), use_container_width=True, hide_index=True)
    
    effective_tax_rate = (total_tax / (fixed_ctc + variable_ctc)) * 100 if (fixed_ctc + variable_ctc) > 0 else 0
    st.info(f"📊 **Effective Tax Rate on Total CTC:** **{effective_tax_rate:.2f}%**")

with tab3:
    st.markdown("#### **Where Does Every Rupee Go? (Total Wealth & Asset Breakdown)**")
    st.markdown("Your total package does not just produce take-home cash—it builds long-term retirement assets:")
    
    total_comp = fixed_ctc + variable_ctc
    total_pf_accrual = employer_pf + employee_pf
    
    wealth_data = [
        {"Asset / Flow Category": "💵 Liquid Cash (Net In-Hand)", "Annual Value": f"₹{annual_total_in_hand:,.0f}", "% of Total CTC": f"{(annual_total_in_hand / total_comp * 100):.1f}%", "Where does it go?": "Directly into your savings bank account"},
        {"Asset / Flow Category": "📈 Retirement: Provident Fund (Employee + Employer)", "Annual Value": f"₹{total_pf_accrual:,.0f}", "% of Total CTC": f"{(total_pf_accrual / total_comp * 100):.1f}%", "Where does it go?": "EPFO Account (earning tax-free ~8.25% interest)"},
        {"Asset / Flow Category": "🏛️ Retirement: NPS Tier 1", "Annual Value": f"₹{employer_nps:,.0f}", "% of Total CTC": f"{(employer_nps / total_comp * 100):.1f}%", "Where does it go?": "NPS PRAN Account (Equity/Debt compound growth)"},
        {"Asset / Flow Category": "🏢 Deferred: Gratuity Provision", "Annual Value": f"₹{gratuity:,.0f}", "% of Total CTC": f"{(gratuity / total_comp * 100):.1f}%", "Where does it go?": "Company Gratuity Trust (paid out upon exiting after 5 yrs)"},
        {"Asset / Flow Category": "⚖️ Statutory Outflow: Taxes (Income Tax + PT)", "Annual Value": f"₹{(total_tax + pt_annual):,.0f}", "% of Total CTC": f"{((total_tax + pt_annual) / total_comp * 100):.1f}%", "Where does it go?": "Government treasury (TDS & State tax)"},
    ]
    
    st.dataframe(pd.DataFrame(wealth_data), use_container_width=True, hide_index=True)
    
    total_retained_wealth = annual_total_in_hand + total_pf_accrual + employer_nps + gratuity
    st.success(
        f"🎯 **Total Realized Economic Value:** You retain **₹{total_retained_wealth:,.0f}** "
        f"(**{(total_retained_wealth / total_comp * 100):.1f}%** of your total CTC) between liquid cash and retirement assets."
    )