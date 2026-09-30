import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os


os.makedirs("charts", exist_ok=True)

df = pd.read_csv("customer_transactions.csv")

df["OrderDate"] = pd.to_datetime(df["OrderDate"])

print("Customer Retention Analysis")
print("---------------------------")
print("Total Transactions:", len(df))
print("Total Customers:", df["CustomerID"].nunique())

analysis_date = pd.Timestamp("2024-12-31")

rfm = df.groupby("CustomerID").agg({
    "OrderDate": ["min", "max", "count"],
    "Amount": "sum"
})

rfm.columns = [
    "FirstPurchase",
    "LastPurchase",
    "Frequency",
    "Monetary"
]

rfm["Recency"] = (
    analysis_date - rfm["LastPurchase"]
).dt.days

rfm = rfm.reset_index()


rfm["Churned"] = (rfm["Recency"] > 180).astype(int)

rfm["R_Score"] = pd.qcut(
    rfm["Recency"].rank(method="first"),
    5,
    labels=[5, 4, 3, 2, 1]
).astype(int)

rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

rfm["M_Score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

def get_segment(row):

    r = row["R_Score"]
    f = row["F_Score"]

    if r >= 4 and f >= 4:
        return "Champions"

    elif r >= 3 and f >= 3:
        return "Loyal Customers"

    elif r >= 4 and f <= 2:
        return "New Customers"

    elif r == 3 and f <= 2:
        return "Promising"

    elif r <= 2 and f >= 4:
        return "Can't Lose Them"

    elif r <= 2 and f == 3:
        return "At Risk"

    elif r <= 2 and f <= 2:
        return "Hibernating / Lost"

    else:
        return "Need Attention"


rfm["Segment"] = rfm.apply(get_segment, axis=1)

rfm.to_csv("rfm_customer_summary.csv", index=False)

segment_summary = rfm.groupby("Segment").agg(
    Customers=("CustomerID", "count"),
    TotalRevenue=("Monetary", "sum"),
    AvgRevenue=("Monetary", "mean"),
    AvgFrequency=("Frequency", "mean"),
    AvgRecency=("Recency", "mean"),
    ChurnedCustomers=("Churned", "sum")
).reset_index()

total_revenue = segment_summary["TotalRevenue"].sum()

segment_summary["RevenueSharePct"] = (
    segment_summary["TotalRevenue"] / total_revenue * 100
).round(2)

segment_summary = segment_summary.sort_values(
    "TotalRevenue",
    ascending=False
)

segment_summary.to_csv("segment_summary.csv", index=False)

df["FirstPurchase"] = df.groupby("CustomerID")["OrderDate"].transform("min")

df["CohortMonth"] = (
    df["FirstPurchase"].dt.to_period("M").dt.to_timestamp()
)

df["OrderMonth"] = (
    df["OrderDate"].dt.to_period("M").dt.to_timestamp()
)

df["CohortPeriod"] = (
    (df["OrderMonth"].dt.year - df["CohortMonth"].dt.year) * 12
    + (df["OrderMonth"].dt.month - df["CohortMonth"].dt.month)
)

cohort_data = df.groupby(
    ["CohortMonth", "CohortPeriod"]
)["CustomerID"].nunique().reset_index()

cohort_table = cohort_data.pivot(
    index="CohortMonth",
    columns="CohortPeriod",
    values="CustomerID"
)

cohort_sizes = cohort_table.iloc[:, 0]

cohort_retention = cohort_table.divide(
    cohort_sizes,
    axis=0
) * 100

cohort_retention = cohort_retention.round(2)

cohort_retention.to_csv("cohort_retention_table.csv")

correlation = rfm[
    ["Recency", "Frequency", "Monetary", "Churned"]
].corr()

correlation.to_csv("correlation_matrix.csv")

segment_counts = rfm["Segment"].value_counts()

plt.figure(figsize=(9, 5))
segment_counts.plot(kind="bar")

plt.title("Customer Segments")
plt.xlabel("Segment")
plt.ylabel("Number of Customers")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

plt.savefig("charts/segment_distribution.png")
plt.close()

revenue_data = segment_summary.sort_values(
    "TotalRevenue",
    ascending=True
)

plt.figure(figsize=(9, 5))
plt.barh(
    revenue_data["Segment"],
    revenue_data["TotalRevenue"]
)

plt.title("Revenue by Customer Segment")
plt.xlabel("Revenue")
plt.ylabel("Segment")
plt.tight_layout()

plt.savefig("charts/revenue_by_segment.png")
plt.close()

plt.figure(figsize=(10, 6))

plt.imshow(
    cohort_retention,
    aspect="auto",
    interpolation="nearest"
)

plt.colorbar(label="Retention %")

plt.title("Customer Cohort Retention")
plt.xlabel("Months Since First Purchase")
plt.ylabel("Cohort")

plt.tight_layout()

plt.savefig("charts/cohort_retention.png")
plt.close()

plt.figure(figsize=(7, 5))

plt.imshow(
    correlation,
    interpolation="nearest",
    aspect="auto"
)

plt.colorbar()

plt.xticks(
    range(len(correlation.columns)),
    correlation.columns,
    rotation=45,
    ha="right"
)

plt.yticks(
    range(len(correlation.columns)),
    correlation.columns
)

plt.title("RFM and Churn Correlation")

plt.tight_layout()

plt.savefig("charts/correlation_heatmap.png")
plt.close()

plt.figure(figsize=(8, 5))

active = rfm[rfm["Churned"] == 0]
churned = rfm[rfm["Churned"] == 1]

plt.scatter(
    active["Recency"],
    active["Frequency"],
    label="Active"
)

plt.scatter(
    churned["Recency"],
    churned["Frequency"],
    label="Churned"
)

plt.title("Recency vs Frequency")
plt.xlabel("Recency (Days)")
plt.ylabel("Frequency")
plt.legend()

plt.tight_layout()

plt.savefig("charts/recency_frequency.png")
plt.close()

total_customers = len(rfm)

churned_customers = rfm["Churned"].sum()

churn_rate = (
    churned_customers / total_customers * 100
)

top_segment = segment_summary.iloc[0]["Segment"]

top_segment_revenue = segment_summary.iloc[0]["TotalRevenue"]

at_risk_count = len(
    rfm[rfm["Segment"] == "At Risk"]
)

lost_count = len(
    rfm[rfm["Segment"] == "Hibernating / Lost"]
)

recency_churn_corr = correlation.loc[
    "Recency", "Churned"
]

frequency_churn_corr = correlation.loc[
    "Frequency", "Churned"
]

monetary_churn_corr = correlation.loc[
    "Monetary", "Churned"
]


report = f"""# Customer Retention Analysis

## Basic Summary

- Total customers: {total_customers}
- Total transactions: {len(df)}
- Churned customers: {churned_customers}
- Churn rate: {churn_rate:.2f}%

## Customer Segments

The segment with the highest revenue is **{top_segment}**.

Revenue from this segment: {top_segment_revenue:.2f}

Customers in the At Risk segment: {at_risk_count}

Customers in the Hibernating / Lost segment: {lost_count}

## Correlation with Churn

- Recency vs Churn: {recency_churn_corr:.2f}
- Frequency vs Churn: {frequency_churn_corr:.2f}
- Monetary vs Churn: {monetary_churn_corr:.2f}

## Main Findings

1. Customers were divided into different groups using RFM analysis.
2. Recency helps identify customers who have not purchased recently.
3. Frequency shows how often customers make purchases.
4. Monetary value shows how much customers have spent.
5. The cohort table shows how customer retention changes over time.
6. The correlation analysis shows the relationship between RFM values and churn.

## Possible Retention Actions

- Contact customers in the At Risk segment with offers or reminders.
- Try to bring back Hibernating / Lost customers.
- Maintain good relationships with Champions and Loyal Customers.
- Study the buying behavior of high-value customers.
"""

with open("insights_report.md", "w") as file:
    file.write(report)


print("\nAnalysis completed successfully!")

print("\nFiles created:")
print("- rfm_customer_summary.csv")
print("- segment_summary.csv")
print("- cohort_retention_table.csv")
print("- correlation_matrix.csv")
print("- insights_report.md")
print("- charts/segment_distribution.png")
print("- charts/revenue_by_segment.png")
print("- charts/cohort_retention.png")
print("- charts/correlation_heatmap.png")
print("- charts/recency_frequency.png")