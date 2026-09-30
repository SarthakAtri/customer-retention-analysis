📊 Customer Retention Analysis
A data analytics project that analyzes customer transaction data to understand customer behavior, identify churn patterns, and evaluate customer retention using RFM Analysis, Cohort Analysis, and Correlation Analysis.

🎯 Project Goal
The goal of this project is to answer business questions such as:
1.Which customers are the most valuable?
2.Which customers are likely to stop purchasing?
3.How does customer retention change over time?
4.What factors are most related to customer churn?

🛠 Tools Used
1.Python
2.Pandas
3.NumPy
4.Matplotlib
5.CSV Dataset

📑 Dataset
This project uses a synthetic customer transaction dataset generated using Python.
 Dataset Features:
• 1,000 customers
• Multiple customer behavior patterns
• Transactions from January 2023 to December 2024
• No real customer data was used

📁 Project Files
customer-retention-analysis/
│
├── generate_customer_data.py
├── customer_retention_analysis.py
├── customer_transactions.csv
├── rfm_customer_summary.csv
├── segment_summary.csv
├── cohort_retention_table.csv
├── correlation_matrix.csv
├── insights_report.md
├── requirements.txt
├── README.md
│
└── charts/
   ├── segment_distribution.png
   ├── revenue_by_segment.png
   ├── cohort_retention_heatmap.png
   ├── correlation_heatmap.png
   └── recency_frequency_scatter.png
📊 Analysis Performed
1.RFM Analysis
Calculated:
•Recency
•Frequency
•Monetary Value

to identify customer purchasing behavior and segment customers.

2.Customer Segmentation
Customers were grouped into:
• Champions
• Loyal Customers
• New Customers
• Promising
• Need Attention
• At Risk
• Can't Lose Them
• Hibernating / Lost

3.Churn Analysis

Customers with no purchases in the last 180 days were marked as churned.

4.Cohort Analysis

Tracked customer retention month by month to understand repeat purchasing behavior.

5.Correlation Analysis

Measured relationships between:
•Recency
•Frequency
•Monetary Value
•Churn
to identify important churn indicators.

📈 Key Insights
•Recency showed the strongest relationship with churn.
•Customers who purchased recently were less likely to churn.
•Champion customers contributed a significant portion of revenue.
•Customer retention gradually decreased over time.
•High-spending customers could still become at risk if they stopped purchasing regularly.

🚀 How to Run
Step 1: Install dependencies
 pip install -r requirements.txt
 Step 2: Generate synthetic customer data
 python generate_customer_data.py
 Step 3: Run customer retention analysis
 python customer_retention_analysis.py

📂Generated outputs include:
•Customer Segments
•Churn Analysis
•Cohort Retention Table
•Correlation Matrix
•Visualizations
•Business Insights Report

📚 Skills Demonstrated
•Data Cleaning
•Exploratory Data Analysis
•RFM Analysis
•Customer Segmentation
•Cohort Analysis
•Correlation Analysis
•Data Visualization
•Business Insight Generation

👨‍💻 Made by Sarthak Atri
Data Analytics | Python | Pandas | Customer Analytics