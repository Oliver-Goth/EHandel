import pandas as pd
import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

server = os.getenv("SQL_SERVER_HOST")
user = os.getenv("SQL_SERVER_USER")
password = os.getenv("SQL_SERVER_PASSWORD")
database = os.getenv("SQL_SERVER_DB")
port = os.getenv("SQL_SERVER_PORT")

# Build connection string
conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=127.0.0.1,{port};DATABASE={database};UID={user};PWD={password}"
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
cursor.fast_executemany = True

print("Connected to:", conn.getinfo(pyodbc.SQL_DATABASE_NAME))


def clear_tables():
    # ⚠️ Delete in order: child tables → parent tables
    cursor.execute("DELETE FROM Product")
    cursor.execute("DELETE FROM [User]")
    cursor.execute("DELETE FROM Category")
    conn.commit()
    print("🧹 Cleared all existing data.")


def insert_categories():
    df = pd.read_csv("data/categories.csv")
    for index, row in df.iterrows():
        cursor.execute("""
            INSERT INTO Category (CategoryID, CategoryName) VALUES (?, ?)
        """, row["CategoryID"], row["Name"])
    conn.commit()
    print("✅ Categories inserted.")


def insert_products():
    df = pd.read_csv("data/products_normalized.csv")
    df = df.drop_duplicates(subset="ProductID")
    print("New shape after dropping duplicates:", df.shape)

    for index, row in df.iterrows():
        cursor.execute("""
            INSERT INTO Product (ProductID, ProductName, Price, Brand, Stock, CategoryID)
            VALUES (?, ?, ?, ?, ?, ?)
        """, row["ProductID"], row["Name"], row["Price"], row["Brand"], row["Stock"], row["categoryId"])
    conn.commit()
    print("✅ Products inserted.")


def insert_users():
    df = pd.read_csv("data/users.csv")

    # 🧼 Clean & normalize emails
    df["email"] = df["email"].astype(str).str.strip().str.lower()

    # 🔍 Drop rows with duplicate emails (keep first)
    df = df.drop_duplicates(subset="email")
    print("New shape after dropping duplicate emails:", df.shape)

    skipped = 0
    for index, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT INTO [User] (UserID, Name, Email, Password, Role)
                VALUES (?, ?, ?, ?, ?)
            """, row["UserID"], row["Name"], row["email"], row["password"], row["role"])
        except pyodbc.IntegrityError as e:
            print(f"⚠️ Skipped duplicate email: {row['email']} (UserID: {row['UserID']})")
            skipped += 1

    conn.commit()
    print(f"✅ Users inserted. Skipped duplicates: {skipped}")



if __name__ == "__main__":
    clear_tables()
    insert_categories()
    insert_products()
    insert_users()
    print("🎉 All data imported successfully!")
