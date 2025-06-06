import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.sql_queries import get_order_history

user_id = 101
history = get_order_history(user_id)

if not history:
    print(f"📭 No orders found for user {user_id}")
else:
    print(f"📦 Order history for user {user_id}:")
    for order_id, details in history.items():
        print(f"\n🧾 Order #{order_id} on {details['order_date']}")
        for item in details["items"]:
            print(f" - {item['quantity']}x {item['name']} (${item['price']})")
