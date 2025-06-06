from pymongo import MongoClient
from datetime import datetime

# Connect to Mongo
client = MongoClient("mongodb://localhost:27017/")
db = client["ehandel"]
reviews = db["reviews"]

# ⭐ NEW: Use numeric IDs (matching SQL)
def add_review(product_id: int, user_id: int, rating: int, comment: str):
    review = {
        "productId": product_id,   # e.g., 1
        "userId": user_id,         # e.g., 65
        "rating": int(rating),
        "comment": comment,
        "createdAt": datetime.utcnow()
    }
    reviews.insert_one(review)
    print("✅ Review submitted.")

# ⭐ Updated to match productId from SQL (int)
def get_avg_rating(product_id: int):
    pipeline = [
        { "$match": { "productId": product_id } },
        { "$group": {
            "_id": "$productId",
            "avgRating": { "$avg": "$rating"},
            "reviewCount": { "$sum": 1 }
        }}
    ]
    result = list(reviews.aggregate(pipeline))
    if result:
        return result[0]
    else:
        return {"avgRating": 0, "reviewCount": 0}

# ⭐ Updated to match productId from SQL (int)
def get_reviews(product_id: int, limit=5):
    cursor = reviews.find({ "productId": product_id }).sort("createdAt", -1).limit(limit)
    return list(cursor)

# --------------------------------------------
# 💡 EXAMPLE USAGE (matching SQL IDs!)
# Product ID 1 = 'Bosch Cordless Drill'
# User ID 65 = from SQL insert
# --------------------------------------------

if __name__ == "__main__":
    product_id = 1   # Matches SQL Product.id
    user_id = 65     # Matches SQL User.id

    # Insert review
    add_review(product_id, user_id, 5, "Very nice product!")

    # Show average
    print("📊 Updated average rating:")
    print(get_avg_rating(product_id))

    # Show reviews
    print("\n📝 Recent reviews:")
    for r in get_reviews(product_id):
        print(f"- userId {r['userId']} rated {r['rating']}★: {r['comment']}")
