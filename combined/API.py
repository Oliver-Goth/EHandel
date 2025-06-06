from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import pyodbc

app = Flask(__name__)
CORS(app)

# Initialize MongoDB client
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['EHandelDB']
reviews_collection = mongo_db['reviews']

def get_connection():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost;DATABASE=EHandelDB;Trusted_Connection=yes;'
    )

def rows_to_dict(cursor, rows):
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in rows]

# CRUD: CATEGORY
@app.route('/api/category', methods=['GET', 'POST'])
def category():
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
@app.route('/api/orderdetail', methods=['GET', 'POST'])
def order_detail_list():
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM OrderDetail")
        return jsonify(rows_to_dict(cursor, cursor.fetchall()))

    if request.method == 'POST':
        data = request.json
        cursor.execute("""
            INSERT INTO OrderDetail (OrderID, ProductID, Quantity, PriceAtPurchase)
            VALUES (?, ?, ?, ?)
        """, data['orderId'], data['productId'], data['quantity'], data['priceAtPurchase'])
        conn.commit()
        return jsonify({"status": "OrderDetail created"}), 201

@app.route('/api/orderdetail/<int:order_detail_id>', methods=['PUT', 'DELETE'])
def order_detail_update(order_detail_id):
    conn = get_connection()
    cursor = conn.cursor()
    if request.method == 'PUT':
        data = request.json
        cursor.execute("""
            UPDATE OrderDetail SET OrderID=?, ProductID=?, Quantity=?, PriceAtPurchase=?
            WHERE OrderDetailID=?
        """, data['orderId'], data['productId'], data['quantity'], data['priceAtPurchase'], order_detail_id)
        conn.commit()
        return jsonify({"status": "OrderDetail updated"})
    elif request.method == 'DELETE':
        cursor.execute("DELETE FROM OrderDetail WHERE OrderDetailID=?", order_detail_id)
        conn.commit()
        return jsonify({"status": "OrderDetail deleted"})

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

if __name__ == '__main__':
    app.run(debug=True)
