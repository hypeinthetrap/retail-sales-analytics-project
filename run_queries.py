import sqlite3
import pandas as pd

DB_PATH = "retail.db"

print("✅ Starting run_queries.py...")

conn = sqlite3.connect(DB_PATH)

# Confirm tables exist
tables = pd.read_sql_query(
    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;",
    conn
)
print("\n📌 Tables in the database:")
print(tables)

query = """
SELECT product_category,
       SUM(total_amount) AS total_revenue
FROM transactions
GROUP BY product_category
ORDER BY total_revenue DESC;
"""


df = pd.read_sql_query(query, conn)

print("\n📌 Preview of transactions (10 rows):")
print(df.to_string(index=False))  # forces full visible print

conn.close()
print("\n📌 Query result:")

