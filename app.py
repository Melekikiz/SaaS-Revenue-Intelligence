import streamlit as st
import pandas as pd
import numpy as np

# Page Configuration
st.set_page_config(page_title="NimbusHR Revenue Intelligence", layout="wide")

st.title("🚀 SaaS Revenue Intelligence Dashboard")
st.markdown("---")

# ===============================
# LOAD DATA
# ===============================

@st.cache_data
def load_data():
    df_cust = pd.read_csv("data/customers.csv")
    df_subs = pd.read_csv("data/subscriptions.csv")
    df_pay = pd.read_csv("data/payments.csv")
    df_mkt = pd.read_csv("data/marketing_spend.csv")

    df = pd.merge(df_cust, df_subs, on="customer_id", how="left")

    df["signup_date"] = pd.to_datetime(df["signup_date"])
    df["start_date"] = pd.to_datetime(df["start_date"])
    df["end_date"] = pd.to_datetime(df["end_date"], errors="coerce")

    df["mrr"] = df["monthly_price"] * df["seats"]
    df["arr"] = df["mrr"] * 12

    return df, df_pay, df_mkt

df, df_payments, df_marketing = load_data()

# ===============================
# SIDEBAR FILTERS
# ===============================

st.sidebar.header("🔍 Global Filters")

plan_filter = st.sidebar.multiselect(
    "Subscription Plan",
    df["plan_type"].unique(),
    default=df["plan_type"].unique()
)

industry_filter = st.sidebar.multiselect(
    "Target Industry",
    df["industry"].unique(),
    default=df["industry"].unique()
)

# Apply Filters
df = df[(df["plan_type"].isin(plan_filter)) & (df["industry"].isin(industry_filter))]
df_active = df[df["end_date"].isna()].copy()

st.sidebar.markdown("---")
st.sidebar.header("🧭 Navigation")
page = st.sidebar.radio(
    "Select Module",
    ["Overview", "Revenue Analysis", "Churn Analysis", "Unit Economics", "Revenue Leakage"]
)

# ===============================
# OVERVIEW
# ===============================

if page == "Overview":
    st.header("📌 Executive Summary")

    total_mrr = df_active["mrr"].sum()
    total_arr = df_active["arr"].sum()
    active_customers = df_active["customer_id"].nunique()
    arpu = total_mrr / active_customers if active_customers else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current MRR", f"${total_mrr:,.0f}")
    col2.metric("Annualized Revenue (ARR)", f"${total_arr:,.0f}")
    col3.metric("Active Base", active_customers)
    col4.metric("ARPU", f"${arpu:,.0f}")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Revenue Contribution by Plan")
        mrr_by_plan = df_active.groupby("plan_type")["mrr"].sum().sort_values(ascending=False)
        st.bar_chart(mrr_by_plan)
        
        if not mrr_by_plan.empty:
            top_plan = mrr_by_plan.idxmax()
            share = (mrr_by_plan.max() / mrr_by_plan.sum()) * 100
            st.info(f"**Strategic Insight:** {top_plan} is your primary growth engine, commanding {share:.1f}% of total revenue. Upselling Basic users to {top_plan} should be a Q3 priority.")

    with col2:
        st.subheader("Market Vertical Performance")
        revenue_industry = df_active.groupby("industry")["mrr"].sum().sort_values(ascending=False)
        st.bar_chart(revenue_industry)
        
        if not revenue_industry.empty:
            top_industry = revenue_industry.idxmax()
            st.success(f"**Market Fit:** Strongest traction in {top_industry}. Consider developing industry-specific features to deepen penetration in this vertical.")

# ===============================
# REVENUE ANALYSIS
# ===============================

elif page == "Revenue Analysis":
    st.header("📈 Growth & Market Segmentation")

    df["start_month"] = df["start_date"].dt.to_period("M").astype(str)
    mrr_trend = df.groupby("start_month")["mrr"].sum()

    st.subheader("Monthly Recurring Revenue Growth")
    st.line_chart(mrr_trend)

    growth = mrr_trend.pct_change().mean() * 100
    st.info(f"**Growth Velocity:** Averaging {growth:.2f}% monthly MRR growth. Maintaining this velocity is key for achieving the next funding milestone.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Revenue by Company Size")
        revenue_size = df_active.groupby("company_size")["mrr"].sum().sort_values(ascending=False)
        st.bar_chart(revenue_size)
        st.markdown("**Observation:** Revenue is heavily concentrated in specific company size segments, indicating a clear 'Ideal Customer Profile' (ICP).")

    with col2:
        st.subheader("Plan Tier Mix")
        revenue_plan = df_active.groupby("plan_type")["mrr"].sum().sort_values(ascending=False)
        st.bar_chart(revenue_plan)

# ===============================
# CHURN ANALYSIS
# ===============================

elif page == "Churn Analysis":
    st.header("📉 Retention & Churn Intelligence")

    lost_customers = df[df["end_date"].notnull()]["customer_id"].nunique()
    total_customers = df["customer_id"].nunique()
    churn_rate = (lost_customers / total_customers * 100) if total_customers else 0

    st.metric("Net Revenue Churn (Lifetime)", f"{churn_rate:.2f}%")

    st.subheader("Churn Probability by Subscription Tier")
    plan_churn = df.groupby("plan_type").apply(
        lambda x: (x[x["end_date"].notnull()]["customer_id"].nunique() / x["customer_id"].nunique()) * 100,
        include_groups=False
    )
    st.bar_chart(plan_churn)
    
    if not plan_churn.empty:
        highest_churn = plan_churn.idxmax()
        st.warning(f"**Retention Risk:** {highest_churn} plan shows significant churn. Investigation into 'Time-to-Value' for these users is recommended.")

    st.subheader("Industry-Specific Attrition Rates")
    industry_churn = df.groupby("industry").apply(
        lambda x: (x[x["end_date"].notnull()]["customer_id"].nunique() / x["customer_id"].nunique()) * 100,
        include_groups=False
    ).sort_values(ascending=False)
    st.bar_chart(industry_churn)
    st.error("**Sector Warning:** Verticals at the top of this chart are leaking revenue. Review customer success touchpoints for these industries.")

# ===============================
# UNIT ECONOMICS
# ===============================

elif page == "Unit Economics":
    st.header("💎 Unit Economics & Profitability")

    plan_metrics = df_active.groupby("plan_type").agg(mrr_sum=("mrr", "sum"), customers=("customer_id", "nunique"))
    plan_metrics["arpu"] = plan_metrics["mrr_sum"] / plan_metrics["customers"]

    plan_churn = df.groupby("plan_type").apply(
        lambda x: (x[x["end_date"].notnull()]["customer_id"].nunique() / x["customer_id"].nunique()),
        include_groups=False
    )
    plan_metrics["churn"] = plan_churn
    plan_metrics["ltv"] = plan_metrics["arpu"] / plan_metrics["churn"].replace(0, np.nan)

    st.subheader("Customer Lifetime Value (LTV) by Tier")
    st.dataframe(plan_metrics.style.format("${:,.2f}", subset=['arpu', 'ltv']).format("{:.2%}", subset=['churn']))

    st.subheader("Customer Acquisition Cost (CAC) by Channel")
    marketing = df_marketing.groupby("channel").agg(spend=("spend", "sum"), customers=("customers_acquired", "sum"))
    marketing["cac"] = marketing["spend"] / marketing["customers"]
    st.bar_chart(marketing["cac"])

    avg_cac = marketing["cac"].mean()
    ltv_cac = plan_metrics["ltv"] / avg_cac

    st.subheader("LTV / CAC Efficiency Ratio")
    st.bar_chart(ltv_cac)
    
    if not ltv_cac.empty:
        best_plan = ltv_cac.idxmax()
        st.success(f"**Profitability Insight:** {best_plan} tier delivers the highest ROI per marketing dollar spent. Scaling this segment provides the safest path to capital efficiency.")

# ===============================
# REVENUE LEAKAGE
# ===============================

elif page == "Revenue Leakage":
    st.header("💸 Revenue Leakage & Payment Health")

    failed = df_payments[df_payments["status"] == "failed"]["amount"].sum()
    refunded = df_payments[df_payments["status"] == "refunded"]["amount"].sum()
    total_potential = df_payments["amount"].sum()

    col1, col2 = st.columns(2)
    col1.metric("Failed Collections", f"${failed:,.0f}", delta="Action Required", delta_color="inverse")
    col2.metric("Refunded Revenue", f"${refunded:,.0f}")

    st.subheader("Payment Transaction Distribution")
    status = df_payments.groupby("status")["amount"].sum().sort_values(ascending=False)
    st.bar_chart(status)

    leakage_rate = ((failed + refunded) / total_potential * 100) if total_potential else 0
    st.error(f"**Financial Leakage Alert:** {leakage_rate:.2f}% of your potential revenue is not reaching the bank account.")

    st.markdown("""
    ### 🛠 Operational Roadmap to Recover Revenue
    * **Involuntary Churn Prevention:** Implement automated **Dunning Management** (email sequences for failed cards).
    * **Payment Retry Logic:** Use AI-driven smart retries to process payments when success probability is highest.
    * **Lock-in Value:** Offer a **15-20% discount on Annual Billing** to bypass monthly transaction failure risks.
    * **Proactive Alerts:** Notify Account Managers immediately when a high-value Enterprise payment fails.
    """)