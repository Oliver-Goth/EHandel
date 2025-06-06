from app.core.sql_queries import get_products_by_ids
from db.redis_connector import get_redis_client
from db.sql_connector import get_sql_connection
from datetime import datetime

r = get_redis_client()

CART_TTL = 1800  # 30 minutes

def add_to_cart(user_id, product_id, quantity=1):
    r = get_redis_client()
    cart_key = f"cart:{user_id}"
    r.hset(cart_key, product_id, quantity)
    r.expire(cart_key, CART_TTL)
    print(f"🛒 Added {quantity}x {product_id} to cart for user {user_id}")

def view_cart(user_id):
    r = get_redis_client()
    cart_key = f"cart:{user_id}"
    cart_data = r.hgetall(cart_key)

    if not cart_data:
        print("🛒 Cart is empty.")
        return []

    # Convert keys and values to proper types
    product_ids = list(cart_data.keys())
    quantities = {k: int(v) for k, v in cart_data.items()}

    # Lookup product details in SQL
    products = get_products_by_ids(product_ids)

    # Merge product info with quantity
    for p in products:
        p["quantity"] = quantities.get(p["id"], 0)

    return products

def checkout(user_id):
    cart_key = f"cart:{user_id}"
    cart = r.hgetall(cart_key)

    if not cart:
        print("❌ Cart was empty – nothing to checkout.")
        return None

    product_ids = list(cart.keys())

    conn = get_sql_connection()
    cursor = conn.cursor()

    # Fetch product prices from SQL
    placeholders = ",".join("?" for _ in product_ids)
    query = f"SELECT ProductID, Price FROM Product WHERE ProductID IN ({placeholders})"
    cursor.execute(query, product_ids)
    price_lookup = {row.ProductID: float(row.Price) for row in cursor.fetchall()}

    # Calculate total
    valid_cart = {
    pid: int(qty)
    for pid, qty in cart.items()
    if pid in price_lookup
    }

    missing_items = [pid for pid in cart if pid not in price_lookup]
    for pid in missing_items:
        print(f"⚠️ Skipping unknown product: {pid}")

    if not valid_cart:
        print("❌ All items in cart were invalid – nothing to checkout.")
        return None

    total = sum(price_lookup[pid] * qty for pid, qty in valid_cart.items())


    # Insert into Order table
    cursor.execute("""
        INSERT INTO [Order] (UserID, OrderDate, Total)
        OUTPUT INSERTED.OrderID
        VALUES (?, GETDATE(), ?)
    """, user_id, total)
    order_id = cursor.fetchone()[0]

    # Insert into OrderItem table
    for pid, qty in valid_cart.items():
        price = price_lookup[pid]
        cursor.execute("""
            INSERT INTO OrderItem (OrderID, ProductID, Quantity, PriceAtPurchase)
            VALUES (?, ?, ?, ?)
        """, order_id, pid, qty, price)

    conn.commit()
    conn.close()

    # Clear cart
    r.delete(cart_key)

    print(f"✅ Order #{order_id} placed successfully for user {user_id}")
    return {
    "order_id": order_id,
    "user_id": user_id,
    "items": valid_cart
}

