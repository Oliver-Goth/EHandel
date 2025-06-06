from db.sql_connector import get_sql_connection

def list_products():
    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ProductID, ProductName, Price FROM Product")
    rows = cursor.fetchall()
    conn.close()

    return [{"id": row.ProductID, "name": row.ProductName, "price": row.Price} for row in rows]

def get_products_by_ids(product_ids):
    conn = get_sql_connection()
    cursor = conn.cursor()

    placeholders = ','.join('?' for _ in product_ids)
    query = f"SELECT ProductID, ProductName, Price FROM Product WHERE ProductID IN ({placeholders})"
    cursor.execute(query, product_ids)

    results = []
    for row in cursor.fetchall():
        results.append({
            "id": row.ProductID,
            "name": row.ProductName,
            "price": row.Price
        })

    conn.close()
    return results

def get_order_history(user_id):
    conn = get_sql_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT o.OrderID, o.OrderDate, oi.ProductID, p.ProductName, oi.Quantity, oi.PriceAtPurchase
        FROM [Order] o
        JOIN OrderItem oi ON o.OrderID = oi.OrderID
        JOIN Product p ON oi.ProductID = p.ProductID
        WHERE o.UserID = ?
        ORDER BY o.OrderDate DESC
    """, user_id)

    rows = cursor.fetchall()
    conn.close()

    history = {}
    for row in rows:
        order_id = row[0]
        if order_id not in history:
            history[order_id] = {
                "order_date": row[1],
                "items": []
            }
        history[order_id]["items"].append({
            "product_id": row[2],
            "name": row[3],
            "quantity": row[4],
            "price": float(row[5])
        })

    return history