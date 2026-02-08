import sqlite3
import pandas as pd

conn = sqlite3.connect("retail.db")

query = """
SELECT
    date,
    product_category,
    customer_id,
    quantity,
    total_amount
FROM transactions
"""

df = pd.read_sql_query(query, conn)

df.to_csv("powerbi_retail_data.csv", index=False)

conn.close()

print("Exported data for Power BI")
