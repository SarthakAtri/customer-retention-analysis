import random
from datetime import datetime, timedelta

import pandas as pd

random.seed(42)

start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)

profiles = {
    "Champion": (100, (0, 300), (15, 35), (1200, 4500), None),
    "Loyal": (200, (0, 400), (25, 55), (700, 2200), None),
    "Regular": (250, (0, 500), (40, 90), (400, 1400), None),
    "AtRisk": (200, (0, 300), (30, 60), (500, 1800), None),
    "New": (150, (640, 730), (20, 45), (400, 1600), (1, 3)),
    "OneTime": (100, (0, 700), (0, 0), (300, 2500), (1, 1))
}

transactions = []
customer_types = []

customer_no = 1
order_no = 1

for customer_type, values in profiles.items():

    count, signup_range, gap_range, amount_range, order_limit = values

    for _ in range(count):

        customer_id = f"CUST{customer_no:05d}"

        signup_date = start_date + timedelta(
            days=random.randint(*signup_range)
        )

        last_active = end_date

        if customer_type == "AtRisk":
            churn_days = random.randint(181, 400)
            last_active = end_date - timedelta(days=churn_days)

        if order_limit:
            max_orders = random.randint(*order_limit)
        else:
            max_orders = 10000

        order_date = signup_date
        orders = 0

        while (
            order_date <= last_active
            and order_date <= end_date
            and orders < max_orders
        ):

            transactions.append({
                "OrderID": f"ORD{order_no:06d}",
                "CustomerID": customer_id,
                "OrderDate": order_date.strftime("%Y-%m-%d"),
                "Amount": round(
                    random.uniform(*amount_range), 2
                )
            })

            order_no += 1
            orders += 1

            if customer_type == "OneTime":
                break

            if gap_range[1] > 0:
                gap = random.randint(*gap_range)
            else:
                gap = 1

            order_date += timedelta(days=gap)

        customer_types.append({
            "CustomerID": customer_id,
            "CustomerType": customer_type
        })

        customer_no += 1


df = pd.DataFrame(transactions)

df = df.sort_values(
    ["OrderDate", "CustomerID"]
)

df.to_csv(
    "customer_transactions.csv",
    index=False
)

pd.DataFrame(customer_types).to_csv(
    "customer_true_types.csv",
    index=False
)

print("Dataset generated successfully!")
print("Customers:", df["CustomerID"].nunique())
print("Transactions:", len(df))

print("\nCustomer Type Distribution:")
print(
    pd.DataFrame(customer_types)["CustomerType"].value_counts()
)

print("\nFiles created:")
print("- customer_transactions.csv")
print("- customer_true_types.csv")