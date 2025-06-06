from db.mongo_connector import get_mongo_collection

def get_product_specs(product_id):
    collection = get_mongo_collection("products")
    return collection.find_one({"productId": product_id})

def get_reviews(product_id):
    reviews_col = get_mongo_collection("reviews")
    results = reviews_col.find({"productId": product_id}, {"_id": 0})  # hide Mongo _id
    return list(results)
