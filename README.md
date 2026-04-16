# SaaS Revenue Intelligence Dashboard
🚀 End-to-End SaaS Financial Analytics Case Study (Python + Streamlit)

NimbusHR is a subscription-based SaaS platform providing HR management solutions for small and medium-sized businesses.
This project simulates a real-world Revenue Intelligence System used by SaaS companies to monitor growth, retention, and profitability.

<img width="1680" height="828" alt="Screenshot 2026-04-16 at 13 51 53" src="https://github.com/user-attachments/assets/224779da-8da9-4108-9fc5-f2b4cf8d0012" />



# 🎯 Business Problem

NimbusHR is experiencing:

Slower-than-expected revenue growth

Increasing customer churn in mid-tier plans

Unclear profitability across customer segments

Rising customer acquisition costs

Key Questions:

Where is revenue growing or leaking?

Which customer segments are most profitable?

What drives churn across plans and industries?

Is the business unit economics sustainable (LTV vs CAC)?


<img width="1680" height="828" alt="Screenshot 2026-04-16 at 13 52 36" src="https://github.com/user-attachments/assets/64049d4e-30f2-4685-80a7-5600e7bc777d" />

# 🧠 Solution

This project builds a full SaaS Revenue Intelligence Dashboard that enables:

Revenue performance tracking (MRR / ARR)

Customer churn analysis

Cohort-based business insights (implicit)

Unit economics (LTV vs CAC)

Revenue leakage detection

Executive-level decision support

# 📦 Dataset Overview (Synthetic but Realistic)

The system uses realistic SaaS simulation datasets:

***👥 Customers***

customer_id

signup_date

industry

company_size

acquisition_channel

***💳 Subscriptions***

plan_type (Basic / Pro / Enterprise)

monthly_price

seats

start_date

end_date

**💰 Payments**

transaction status (paid / failed / refunded)

revenue tracking & leakage analysis

**📣 Marketing Spend**

channel-based acquisition cost

CAC calculation support

**📈 Key Metrics Implemented**

Revenue Metrics

MRR (Monthly Recurring Revenue)

ARR (Annual Recurring Revenue)

ARPU (Average Revenue Per User)

Retention Metrics

Customer churn rate

Plan-based churn segmentation

Industry-based churn analysis

Unit Economics

Customer Lifetime Value (LTV)

Customer Acquisition Cost (CAC)

LTV / CAC ratio

Revenue Health

Payment failure rate

Refund impact

Revenue leakage %

<img width="1680" height="828" alt="Screenshot 2026-04-16 at 13 52 56" src="https://github.com/user-attachments/assets/69087f9d-601f-4965-ac3a-ef1dba388935" />


**📊 Dashboard Features (Streamlit App)**

The dashboard includes 5 analytical modules:

1️⃣ Overview


Real-time SaaS KPIs

Revenue distribution by plan

Market segmentation insights

2️⃣ Revenue Analysis

MRR growth trends

Revenue by company size

Plan contribution breakdown

3️⃣ Churn Analysis

Overall churn rate

Churn by plan type

Industry-based retention risks

4️⃣ Unit Economics

LTV by segment

CAC by acquisition channel

LTV / CAC efficiency ratio

5️⃣ Revenue Leakage

Failed payments analysis

Refund impact

Revenue loss estimation

Recovery recommendations

🛠 Tech Stack

Python 🐍

Pandas

NumPy

Streamlit

Data-driven business analytics


# 📌 Key Business Insights (Example Outputs)

Pro plan shows highest churn → possible value mismatch

Enterprise segment generates highest LTV

LinkedIn acquisition has highest CAC

Manufacturing sector shows elevated churn risk

~X% revenue leakage due to failed payments

📷 How to Run

# Install dependencies

pip install streamlit pandas numpy



# Run app
streamlit run app.py
🧠 Project Goal

This project is designed to simulate a real SaaS analytics environment where:

“Data is not just reported — it drives revenue decisions.”

📌 Author Notes

This project demonstrates:

End-to-end SaaS analytics pipeline

Business-focused data storytelling

KPI engineering

Executive dashboard design

**🔥 What Makes This Project Strong**

✔ Real SaaS business logic

✔ Revenue + churn + CAC + LTV integration

✔ Executive-ready insights

✔ Interactive dashboard

✔ Production-style structure

**🚀 Future Improvements**

Cohort retention heatmaps

Predictive churn modeling

Customer segmentation (clustering)

Subscription upgrade/downgrade tracking

---

### Author
Melek İkiz
