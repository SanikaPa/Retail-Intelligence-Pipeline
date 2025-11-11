import pandas as pd
import matplotlib.pyplot as plt
import os

# -------------------------------
# Paths
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURATED_DIR = os.path.join(BASE_DIR, "data", "curated")
REPORT_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

# -------------------------------
# Load curated CSVs
# -------------------------------
customer_summary = pd.read_csv(os.path.join(CURATED_DIR, "customer_summary.csv"))
product_summary = pd.read_csv(os.path.join(CURATED_DIR, "product_summary.csv"))
monthly_summary = pd.read_csv(os.path.join(CURATED_DIR, "monthly_summary.csv"))
country_summary = pd.read_csv(os.path.join(CURATED_DIR, "country_summary.csv"))

# -------------------------------
# KPI Summary
# -------------------------------
total_revenue = product_summary["TotalRevenue"].sum()
total_orders = monthly_summary["MonthlyOrders"].sum()
avg_order_value = total_revenue / total_orders if total_orders != 0 else 0

kpi_df = pd.DataFrame({
    "TotalRevenue": [total_revenue],
    "TotalOrders": [total_orders],
    "AverageOrderValue": [round(avg_order_value, 2)]
})
kpi_df.to_csv(os.path.join(REPORT_DIR, "kpi_summary.csv"), index=False)

# -------------------------------
# Top customers & products
# -------------------------------
top_customers = customer_summary.sort_values(by="LifetimeValue", ascending=False).head(10)
top_products = product_summary.sort_values(by="TotalRevenue", ascending=False).head(10)

top_customers.to_csv(os.path.join(REPORT_DIR, "top_customers.csv"), index=False)
top_products.to_csv(os.path.join(REPORT_DIR, "top_products.csv"), index=False)

# -------------------------------
# Monthly revenue trend
# -------------------------------
monthly_summary["YearMonth"] = monthly_summary["YEAR"].astype(str) + "-" + monthly_summary["MONTH"].astype(str).str.zfill(2)
plt.figure(figsize=(10,6))
plt.plot(monthly_summary["YearMonth"], monthly_summary["MonthlyRevenue"], marker='o')
plt.xticks(rotation=45)
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Monthly Revenue")
plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, "monthly_revenue_trend.png"))
plt.close()

# -------------------------------
# Revenue by country
# -------------------------------
plt.figure(figsize=(10,6))
plt.bar(country_summary["COUNTRY"], country_summary["TotalRevenue"])
plt.xticks(rotation=45)
plt.title("Revenue by Country")
plt.xlabel("Country")
plt.ylabel("Total Revenue")
plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, "revenue_by_country.png"))
plt.close()

# -------------------------------
# Save Excel report
# -------------------------------
with pd.ExcelWriter(os.path.join(REPORT_DIR, "retail_report.xlsx")) as writer:
    kpi_df.to_excel(writer, sheet_name="KPIs", index=False)
    top_customers.to_excel(writer, sheet_name="TopCustomers", index=False)
    top_products.to_excel(writer, sheet_name="TopProducts", index=False)
    monthly_summary.to_excel(writer, sheet_name="MonthlySummary", index=False)
    country_summary.to_excel(writer, sheet_name="CountrySummary", index=False)

print(f"✅ Reports created successfully in: {os.path.abspath(REPORT_DIR)}")
