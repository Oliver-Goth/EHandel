import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.cart_actions import checkout

user_id = 101
result = checkout(user_id)
print("Order ID:", result)

if result:
    print(f"✅ Order #{result['order_id']} placed by user {result['user_id']}")
    print("📦 Items:")
    for pid, qty in result["items"].items():
        print(f"  - {qty}x {pid}")
else:
    print("❌ Cart was empty – nothing to checkout.")