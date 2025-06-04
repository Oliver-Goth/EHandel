#%%
from pymongo import MongoClient
from faker import Faker
from random import randint, choice
import datetime

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ehandel"]
reviews = db["reviews"]

# Fake data setup
fake = Faker()

# Replace with real productIds if you have them
product_ids = [f"P{str(i).zfill(3)}" for i in range(1, 11)]  # e.g., P001–P010

# Generate reviews
review_docs = []
for _ in range(300):
    review = {
        "productId": choice(product_ids),
        "userName": fake.user_name(),
        "rating": randint(1, 5),
        "comment": fake.sentence(nb_words=12),
        "createdAt": fake.date_time_between(start_date='-6M', end_date='now')
    }
    review_docs.append(review)

# Insert into MongoDB
reviews.insert_many(review_docs)
print("Inserted 300+ fake reviews into ecommerce.reviews")

# %%
