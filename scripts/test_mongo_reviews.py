import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.mongo_queries import get_reviews

product_id = "B08QX1CC14"

print(f"\n🗣️ Reviews for {product_id}:")
reviews = get_reviews(product_id)
if reviews:
    for r in reviews[:3]:
        print(f"- {r['username']} ({r['rating']}★): {r['reviewTitle']}")
else:
    print("No reviews found.")

    