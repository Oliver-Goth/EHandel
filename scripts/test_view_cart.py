import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.cart_actions import view_cart

cart_items = view_cart(101)
for item in cart_items:
    print(f"{item['quantity']}x {item['name']} - ${item['price']}")
