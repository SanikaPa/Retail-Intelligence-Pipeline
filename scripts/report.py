import pandas as pd
import matplotlib.pyplot as plt
import os

# === 1. Paths ===
curated_path = "../data/curated/"
report_path = "../reports/"
os.makedirs(report_path, exist_ok=True)

# === 2. Load curated CSVs ===
customer_summary = pd.read_csv(os.path.join(curated_path, "customer_summary.csv"))
product_summary = pd.read_csv(os.path.join(curated_path, "product_summary.csv"))
monthly_summary = pd.read_csv(os.path.join(curated_path, "monthly_summary.csv"))
country_summary = pd.read_csv(os.path.join(curated_path, "country_summary.csv"))

# === 3. KPI Summary ===
total_revenue = product_summary["TotalRevenue"].sum()
total_orders = monthly_summary["MonthlyOrders"].sum()
avg_order_value = total_revenue / total_orders if total_orders != 0 else 0

kpi_df = pd.DataFrame({
    "TotalRevenue": [total_revenue],
    "TotalOrders": [total_orders],
    "AverageOrderValue": [round(avg_order_value, 2)]
})
kpi_df.to_csv(os.path.join(report_path, "kpi_summary.csv"), index=False)

# === 4. Top Customers by Lifetime Value ===
top_customers = customer_summary.sort_values(by="LifetimeValue", ascending=False).head(10)
top_customers.to_csv(os.path.join(report_path, "top_customers.csv"), index=False)

# === 5. Top Products by Total Revenue ===
top_products = product_summary.sort_values(by="TotalRevenue", ascending=False).head(10)
top_products.to_csv(os.path.join(report_path, "top_products.csv"), index=False)

# === 6. Monthly Revenue Trend ===
monthly_summary["YearMonth"] = monthly_summary["YEAR"].astype(str) + "-" + monthly_summary["MONTH"].astype(str).str.zfill(2)
plt.figure(figsize=(10,6))
plt.plot(monthly_summary["YearMonth"], monthly_summary["MonthlyRevenue"], marker='o')
plt.xticks(rotation=45)
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Monthly Revenue")
plt.tight_layout()
plt.savefig(os.path.join(report_path, "monthly_revenue_trend.png"))
plt.close()

# === 7. Revenue by Country ===
plt.figure(figsize=(10,6))
plt.bar(country_summary["COUNTRY"], country_summary["TotalRevenue"])
plt.xticks(rotation=45)
plt.title("Revenue by Country")
plt.xlabel("Country")
plt.ylabel("Total Revenue")
plt.tight_layout()
plt.savefig(os.path.join(report_path, "revenue_by_country.png"))
plt.close()

# === 8. Save all as Excel Report ===
with pd.ExcelWriter(os.path.join(report_path, "retail_report.xlsx")) as writer:
    kpi_df.to_excel(writer, sheet_name="KPIs", index=False)
    top_customers.to_excel(writer, sheet_name="TopCustomers", index=False)
    top_products.to_excel(writer, sheet_name="TopProducts", index=False)
    monthly_summary.to_excel(writer, sheet_name="MonthlySummary", index=False)
    country_summary.to_excel(writer, sheet_name="CountrySummary", index=False)

print("✅ Reports created successfully in:", os.path.abspath(report_path))
