import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.cart_actions import add_to_cart

add_to_cart(101, "B08QX1CC14", 1)
add_to_cart(101, "B000QJDUSKY", 2)