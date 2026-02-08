import pandas as pd
import sqlite3

CSV_PATH = "data/retail_sales_dataset.csv"
DB_PATH = "retail.db"

# 1) Load CSV
df = pd.read_csv(CSV_PATH)

# 2) Clean / standardize column names (optional but helps)
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

# Expected columns after rename:
# transaction_id, date, customer_id, gender, age, product_category, quantity, price_per_unit, total_amount

# 3) Parse date into a consistent format (YYYY-MM-DD)
df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date.astype(str)

# 4) Connect to SQLite (this creates retail.db if it doesn't exist)
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# 5) Create tables (drop first to avoid duplicates while you iterate)
cur.executescript("""
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;

CREATE TABLE customers (
  customer_id TEXT PRIMARY KEY,
  gender TEXT,
  age INTEGER
);

CREATE TABLE products (
  product_category TEXT PRIMARY KEY
);

CREATE TABLE transactions (
  transaction_id INTEGER PRIMARY KEY,
  date TEXT,
  customer_id TEXT,
  product_category TEXT,
  quantity INTEGER,
  price_per_unit REAL,
  total_amount REAL,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
  FOREIGN KEY (product_category) REFERENCES products(product_category)
);
""")

# 6) Insert customers (deduplicate)
customers = df[["customer_id", "gender", "age"]].drop_duplicates(subset=["customer_id"])
customers.to_sql("customers", conn, if_exists="append", index=False)

# 7) Insert products (deduplicate)
products = df[["product_category"]].drop_duplicates()
products.to_sql("products", conn, if_exists="append", index=False)

# 8) Insert transactions
tx = df[[
    "transaction_id", "date", "customer_id", "product_category",
    "quantity", "price_per_unit", "total_amount"
]]
tx.to_sql("transactions", conn, if_exists="append", index=False)

# 9) Quick sanity checks
print("Rows in customers:", cur.execute("SELECT COUNT(*) FROM customers;").fetchone()[0])
print("Rows in products:", cur.execute("SELECT COUNT(*) FROM products;").fetchone()[0])
print("Rows in transactions:", cur.execute("SELECT COUNT(*) FROM transactions;").fetchone()[0])

conn.commit()
conn.close()

print(f"✅ Built SQLite database: {DB_PATH}")
