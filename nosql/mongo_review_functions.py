from pymongo import MongoClient
from datetime import datetime

# Connect to Mongo
client = MongoClient("mongodb://localhost:27017/")
db = client["ehandel"]
reviews = db["reviews"]

def get_avg_rating(product_id):
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
    
def add_review(product_id, user_name, rating, comment):
    review = {
        "productId": product_id,
        "userName": user_name,
        "rating": int(rating),
        "comment": comment,
        "createdAt": datetime.utcnow()
    }
    reviews.insert_one(review)
    print("✅ Review submitted.")

def get_reviews(product_id, limit=5):
    cursor = reviews.find({ "productId": product_id }).sort("createdAt", -1).limit(limit)
    return list(cursor)
    
if __name__ == "__main__":
    #product_id = "P002"
    #print(get_avg_rating(product_id))
    #print(get_reviews("P002"))
    product_id = "P002"

    # Test: Insert a new review
    add_review(product_id, "bob123", 5, "Very nice product!")

    # Test: Show average rating after insert
    print("📊 Updated average rating:")
    print(get_avg_rating(product_id))

    # Test: Show recent reviews
    print("\n📝 Recent reviews:")
    for r in get_reviews(product_id):
        print(f"- {r['userName']} rated {r['rating']}★: {r['comment']}")