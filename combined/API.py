from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import pyodbc
import traceback
import redis

app = Flask(__name__)
CORS(app)

# Initialize MongoDB client
mongo_client = MongoClient('mongodb://127.0.0.1:27017/')
mongo_db = mongo_client['EHandelDB']
reviews_collection = mongo_db['reviews']

# Initialize SQL client
def get_connection():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=127.0.0.1,1433;DATABASE=shopsmart;UID=sa;PWD=YourStrong!Passw0rd;'
    )

# Initialize Redis client
redis_client = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

CART_TTL = 1800

def rows_to_dict(cursor, rows):
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in rows]

def get_products_by_ids(product_ids):
    conn = get_connection()
    cursor = conn.cursor()
    placeholders = ",".join("?" for _ in product_ids)
    cursor.execute(f"SELECT ProductID as id, ProductName as Name, Price, Stock FROM Product WHERE ProductID IN ({placeholders})", product_ids)
    return rows_to_dict(cursor, cursor.fetchall())

# CRUD: CATEGORY
@app.route('/api/category', methods=['GET', 'POST'])
def category():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        if request.method == 'GET':
            cursor.execute("SELECT * FROM Category")
            return jsonify(rows_to_dict(cursor, cursor.fetchall()))

        if request.method == 'POST':
            data = request.json
            cursor.execute("INSERT INTO Category (Name) VALUES (?)", data['name'])
            conn.commit()
            return jsonify({"status": "Category created"}), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/category/<int:category_id>', methods=['PUT', 'DELETE'])
def category_detail(category_id):
    conn = get_connection()
    cursor = conn.cursor()
    if request.method == 'PUT':
        data = request.json
        cursor.execute("UPDATE Category SET Name=? WHERE CategoryID=?", data['name'], category_id)
        conn.commit()
        return jsonify({"status": "Category updated"})
    elif request.method == 'DELETE':
        cursor.execute("DELETE FROM Category WHERE CategoryID=?", category_id)
        conn.commit()
        return jsonify({"status": "Category deleted"})

# CRUD: PRODUCT
@app.route('/api/product', methods=['GET', 'POST'])
def product():
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM Product")
        return jsonify(rows_to_dict(cursor, cursor.fetchall()))

    if request.method == 'POST':
        data = request.json
        cursor.execute("""
            INSERT INTO Product (Name, Price, Stock, CategoryID)
            VALUES (?, ?, ?, ?)
        """, data['name'], data['price'], data['stock'], data['categoryId'])
        conn.commit()
        return jsonify({"status": "Product created"}), 201

@app.route('/api/product/<int:product_id>', methods=['PUT', 'DELETE'])
def product_detail(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    if request.method == 'PUT':
        data = request.json
        cursor.execute("""
            UPDATE Product SET Name=?, Price=?, Stock=?, CategoryID=?
            WHERE ProductID=?
        """, data['name'], data['price'], data['stock'], data['categoryId'], product_id)
        conn.commit()
        return jsonify({"status": "Product updated"})
    elif request.method == 'DELETE':
        cursor.execute("DELETE FROM Product WHERE ProductID=?", product_id)
        conn.commit()
        return jsonify({"status": "Product deleted"})

# CRUD: ORDER
@app.route('/api/order', methods=['GET', 'POST'])
def order():
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM [Order]")
        return jsonify(rows_to_dict(cursor, cursor.fetchall()))

    if request.method == 'POST':
        data = request.json
        cursor.execute("""
            INSERT INTO [Order] (UserID, OrderDate, Total)
            VALUES (?, ?, ?)
        """, data['userId'], data['orderDate'], data['total'])
        conn.commit()
        return jsonify({"status": "Order created"}), 201

@app.route('/api/order/<int:order_id>', methods=['PUT', 'DELETE'])
def order_detail(order_id):
    conn = get_connection()
    cursor = conn.cursor()
    if request.method == 'PUT':
        data = request.json
        cursor.execute("""
            UPDATE [Order] SET UserID=?, OrderDate=?, Total=?
            WHERE OrderID=?
        """, data['userId'], data['orderDate'], data['total'], order_id)
        conn.commit()
        return jsonify({"status": "Order updated"})
    elif request.method == 'DELETE':
        cursor.execute("DELETE FROM [Order] WHERE OrderID=?", order_id)
        conn.commit()
        return jsonify({"status": "Order deleted"})

# CRUD: ORDER DETAIL
@app.route('/api/orderitem', methods=['GET', 'POST'])
def order_detail_list():
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM OrderItem")
        return jsonify(rows_to_dict(cursor, cursor.fetchall()))

    if request.method == 'POST':
        data = request.json
        cursor.execute("""
            INSERT INTO OrderItem (OrderID, ProductID, Quantity, PriceAtPurchase)
            VALUES (?, ?, ?, ?)
        """, data['orderId'], data['productId'], data['quantity'], data['priceAtPurchase'])
        conn.commit()
        return jsonify({"status": "OrderItem created"}), 201

@app.route('/api/orderitem/<int:order_item_id>', methods=['PUT', 'DELETE'])
def order_item_update(order_item_id):
    conn = get_connection()
    cursor = conn.cursor()
    if request.method == 'PUT':
        data = request.json
        cursor.execute("""
            UPDATE OrderItem SET OrderID=?, ProductID=?, Quantity=?, PriceAtPurchase=?
            WHERE OrderItemID=?
        """, data['orderId'], data['productId'], data['quantity'], data['priceAtPurchase'], order_item_id)
        conn.commit()
        return jsonify({"status": "OrderItem updated"})
    elif request.method == 'DELETE':
        cursor.execute("DELETE FROM OrderItem WHERE OrderItemID=?", order_item_id)
        conn.commit()
        return jsonify({"status": "OrderItem deleted"})

# CRUD: USER
@app.route('/api/user', methods=['GET', 'POST'])
def user():
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM [User]")
        return jsonify(rows_to_dict(cursor, cursor.fetchall()))

    if request.method == 'POST':
        data = request.json
        cursor.execute("""
            INSERT INTO [User] (Name, Email, Password, Role)
            VALUES (?, ?, ?, ?)
        """, data['name'], data['email'], data['password'], data['role'])
        conn.commit()
        return jsonify({"status": "User created"}), 201

@app.route('/api/user/<int:user_id>', methods=['PUT', 'DELETE'])
def user_detail(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    if request.method == 'PUT':
        data = request.json
        cursor.execute("""
            UPDATE [User] SET Name=?, Email=?, Password=?, Role=?
            WHERE UserID=?
        """, data['name'], data['email'], data['password'], data['role'], user_id)
        conn.commit()
        return jsonify({"status": "User updated"})
    elif request.method == 'DELETE':
        cursor.execute("DELETE FROM [User] WHERE UserID=?", user_id)
        conn.commit()
        return jsonify({"status": "User deleted"})
    
# CRUD: REVIEW
@app.route('/api/review', methods=['POST'])
def submit_review():
    data = request.json
    product_id = data.get('productId')
    user_id = data.get('userId')
    rating = data.get('rating')
    comment = data.get('comment')

    # Fetch user name from SQL Server
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Name FROM [User] WHERE UserID = ?", user_id)
    row = cursor.fetchone()
    conn.close()

    if row:
        user_name = row[0]
        # Insert review into MongoDB
        review = {
            'productId': product_id,
            'userId': user_id,
            'userName': user_name,
            'rating': rating,
            'comment': comment,
            'createdAt': datetime.utcnow()  # Store in UTC for consistency
        }
        reviews_collection.insert_one(review)
        return jsonify({"status": "Review submitted"}), 201
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/api/review/<product_id>', methods=['GET'])
def get_reviews(product_id):
    try:
        product_id = int(product_id)  # Convert to int for proper matching
    except ValueError:
        return jsonify({"error": "Invalid product ID"}), 400

    reviews = list(reviews_collection.find({'productId': product_id}))
    for review in reviews:
        review['_id'] = str(review['_id'])  # Convert ObjectId to string for JSON serialization
        if 'createdAt' in review:
            review['createdAt'] = review['createdAt'].isoformat()  # Optional: Format datetime
    return jsonify(reviews)

# ADD TO CART
@app.route('/api/cart', methods=['POST'])
def add_to_cart():
    data = request.json
    user_id = str(data['userId'])
    product_id = str(data['productId'])
    quantity = int(data.get('quantity', 1))

    cart_key = f"cart:{user_id}"
    redis_client.hset(cart_key, product_id, quantity)
    redis_client.expire(cart_key, CART_TTL)

    return jsonify({"status": f"Added {quantity} of product {product_id} to cart"}), 200


# VIEW CART
@app.route('/api/cart/<user_id>', methods=['GET'])
def view_cart(user_id):
    cart_key = f"cart:{user_id}"
    cart_data = redis_client.hgetall(cart_key)

    # Decode Redis keys and values
    quantities = {
        pid.decode() if isinstance(pid, bytes) else pid: int(qty.decode() if isinstance(qty, bytes) else qty)
        for pid, qty in cart_data.items()
    }

    product_ids = list(quantities.keys())

    # Fetch products by their string IDs, adjust your SQL query accordingly
    products = get_products_by_ids(product_ids)  # Make sure this function queries by string IDs, not int

    # Combine product info with quantities
    cart_items = []
    for product in products:
        pid = product['ProductID']  # or 'id', depending on your SQL result keys
        cart_items.append({
            'productId': pid,
            'name': product['ProductName'],
            'price': product['Price'],
            'quantity': quantities.get(pid, 0)
        })

    return jsonify(cart_items), 200


# CHECKOUT
@app.route('/api/cart/checkout/<user_id>', methods=['POST'])
def checkout(user_id):
    cart_key = f"cart:{user_id}"
    cart = redis_client.hgetall(cart_key)

    if not cart:
        return jsonify({"error": "Cart is empty"}), 400

    # Decode keys and values
    quantities = {
        pid.decode() if isinstance(pid, bytes) else pid: int(qty.decode() if isinstance(qty, bytes) else qty)
        for pid, qty in cart.items()
    }

    product_ids = list(quantities.keys())

    conn = get_connection()
    cursor = conn.cursor()

    placeholders = ",".join("?" for _ in product_ids)
    # Query products by string IDs
    cursor.execute(f"SELECT ProductID, Price FROM Product WHERE ProductID IN ({placeholders})", product_ids)
    price_lookup = {row.ProductID: float(row.Price) for row in cursor.fetchall()}

    valid_cart = {
        pid: qty for pid, qty in quantities.items() if pid in price_lookup
    }

    if not valid_cart:
        return jsonify({"error": "All products in cart were invalid"}), 400

    total = sum(price_lookup[pid] * qty for pid, qty in valid_cart.items())

    cursor.execute("""
        INSERT INTO [Order] (UserID, OrderDate, Total)
        OUTPUT INSERTED.OrderID
        VALUES (?, GETDATE(), ?)
    """, user_id, total)
    order_id = cursor.fetchone()[0]

    for pid, qty in valid_cart.items():
        cursor.execute("""
            INSERT INTO OrderItem (OrderID, ProductID, Quantity, PriceAtPurchase)
            VALUES (?, ?, ?, ?)
        """, order_id, pid, qty, price_lookup[pid])

    conn.commit()
    conn.close()

    redis_client.delete(cart_key)

    return jsonify({
        "status": f"Order #{order_id} created",
        "orderId": order_id,
        "items": valid_cart
    }), 201

if __name__ == '__main__':
    app.run(debug=True)
