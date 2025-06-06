import requests

API_BASE_URL = "http://localhost:5000/api"

def print_line():
    print("-" * 40)
    

# ------------------------
# SQL Server: E-handel
# ------------------------

def fetch_categories():
    res = requests.get(f"{API_BASE_URL}/category")
    return res.json() if res.status_code == 200 else []

def fetch_products(category_id=None):
    res = requests.get(f"{API_BASE_URL}/product")
    if res.status_code != 200:
        return []

    all_products = res.json()
    if category_id:
        return [p for p in all_products if p['CategoryID'] == category_id]
    return all_products

def fetch_product_details(product_id):
    products = fetch_products()
    for product in products:
        if product['ProductID'] == product_id:
            return product
    return None

# ------------------------
# MongoDB: Reviews (via API_BASE_URL)
# ------------------------

def add_review(product_id, user_id, rating, comment):
    payload = {
        "productId": product_id,
        "userId": user_id,
        "rating": int(rating),
        "comment": comment
    }
    res = requests.post(f"{API_BASE_URL}/review", json=payload)
    if res.status_code == 201:
        print("✅ Review submitted.")
    else:
        print(f"⚠️ Failed to submit review. Status: {res.status_code}")

def get_reviews(product_id):
    res = requests.get(f"{API_BASE_URL}/review/{product_id}")
    if res.status_code == 200:
        return res.json()
    else:
        print("⚠️ Could not fetch reviews.")
        return []

def get_avg_rating(product_id):
    res = requests.get(f"{API_BASE_URL}/review/{product_id}/average")
    if res.status_code == 200:
        return res.json()
    else:
        return {"avgRating": 0, "reviewCount": 0}

# ------------------------
# UI Logic
# ------------------------

def browse_products():
    categories = fetch_categories()
    while True:
        print_line()
        print("BROWSE CATEGORIES:")
        for idx, cat in enumerate(categories, 1):
            print(f"{idx}. {cat['Name']}")
        print("0. Show all products")
        print("B. Back to main menu")
        print_line()
        choice = input("Choose category (number): ").strip().lower()
        if choice == "b":
            return
        elif choice == "0":
            show_products()
        elif choice.isdigit() and 1 <= int(choice) <= len(categories):
            category = categories[int(choice) - 1]
            show_products(category['CategoryID'])
        else:
            print("Invalid choice.")

def show_products(category_id=None):
    products = fetch_products(category_id)
    while True:
        print_line()
        print("PRODUCT LIST:")
        for idx, p in enumerate(products, 1):
            print(f"{idx}. {p['Name']} - {p['Price']} DKK ({p['Stock']} in stock)")
        print("B. Back")
        print_line()
        choice = input("Select a product to view details: ").strip().lower()
        if choice == "b":
            return
        elif choice.isdigit() and 1 <= int(choice) <= len(products):
            product = products[int(choice) - 1]
            product_details_menu(product['ProductID'])
        else:
            print("Invalid choice.")

def product_details_menu(product_id):
    product = fetch_product_details(product_id)
    if not product:
        print("Product not found.")
        return

    while True:
        print_line()
        print(f"PRODUCT DETAILS")
        print(f"Name: {product['Name']}")
        print(f"Price: {product['Price']} DKK")
        print(f"Stock: {product['Stock']}")
        print(f"Category ID: {product['CategoryID']}")
        print(f"Product ID: {product['ProductID']}")
        print_line()
        print("1. Submit a review")
        print("2. View recent reviews")
        print("3. View average rating")
        print("B. Back to product list")
        choice = input("Choose an option: ").strip().lower()

        if choice == "1":
            UserID = int(input("Your User ID: "))
            rating = input("Rating (1–5): ")
            comment = input("Your review: ")
            add_review(product_id, UserID, rating, comment)

        elif choice == "2":
            print(f"\nRecent reviews for {product_id}:")
            reviews = get_reviews(product_id)
            for r in reviews:
                print(f"- User {r['userId']} rated {r['rating']}★: {r['comment']}")

        elif choice == "3":
            result = get_avg_rating(product_id)
            print(f"\n📊 Product {product_id}:")
            print(f"⭐ Average Rating: {round(result['avgRating'], 2)}")
            print(f"🗳️ Total Reviews: {result['reviewCount']}")

        elif choice == "b":
            return
        else:
            print("Invalid choice.")

def main_menu():
    while True:
        print_line()
        print("E-HANDEL TERMINAL SYSTEM")
        print("1. Browse Products")
        print("2. Exit")
        print_line()
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            browse_products()
        elif choice == "2":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main_menu()
