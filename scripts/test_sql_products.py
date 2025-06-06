import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.sql_queries import list_products

print("🛍️ Available Products:")
for product in list_products():
    print(f"{product['id']} | {product['name']} - ${product['price']}")