import requests

API_BASE_URL = "http://localhost:5000/api"
USER_ID = None

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

def fetch_product_items(product_id):
    products = fetch_products()
    for product in products:
        if product['ProductID'] == product_id:
            return product
    return None

# ------------------------
# MongoDB: Reviews
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
# Redis: Cart
# ------------------------

def add_to_cart(user_id, product_id, quantity):
    payload = {
        "userId": user_id,
        "productId": product_id,
        "quantity": quantity
    }
    res = requests.post(f"{API_BASE_URL}/cart", json=payload)
    if res.status_code == 200:
        print("✅ Product added to cart.")
    else:
        print("⚠️ Failed to add product to cart.")

def get_cart(user_id):
    res = requests.get(f"{API_BASE_URL}/cart/{user_id}")
    if res.status_code == 200:
        return res.json()
    else:
        print("⚠️ Failed to fetch cart.")
        return []

def remove_from_cart(user_id, product_id):
    payload = {
        "userId": user_id,
        "productId": product_id
    }
    res = requests.post(f"{API_BASE_URL}/cart/remove", json=payload)
    if res.status_code == 200:
        print("✅ Product removed from cart.")
    else:
        print("⚠️ Failed to remove product from cart.")

# ------------------------
# UI Logic
# ------------------------

def browse_products():
    categories = fetch_categories()
    while True:
        print_line()
        print("BROWSE CATEGORIES:")
        for idx, cat in enumerate(categories, 1):
            print(f"{idx}. {cat['CategoryName']}")
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
            print(f"{idx}. {p['ProductName']} - {p['Price']} DKK ({p['Stock']} in stock)")
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
    product = fetch_product_items(product_id)
    if not product:
        print("Product not found.")
        return

    while True:
        print_line()
        print(f"PRODUCT DETAILS")
        print(f"Name: {product['ProductName']}")
        print(f"Price: {product['Price']} DKK")
        print(f"Stock: {product['Stock']}")
        print(f"Category ID: {product['CategoryID']}")
        print(f"Product ID: {product['ProductID']}")
        print_line()
        print("1. Add to cart")
        print("2. View cart")
        print("3. Submit a review")
        print("4. View recent reviews")
        print("5. View average rating")
        print("B. Back to product list")
        choice = input("Choose an option: ").strip().lower()

        if choice == "1":
            qty = input("Quantity to add: ")
            if qty.isdigit() and int(qty) > 0:
                add_to_cart(USER_ID, product_id, int(qty))
            else:
                print("Invalid quantity.")

        elif choice == "2":
            show_cart()

        elif choice == "3":
            rating = input("Rating (1–5): ")
            comment = input("Your review: ")
            add_review(product_id, USER_ID, rating, comment)

        elif choice == "4":
            print(f"\nRecent reviews for {product_id}:")
            reviews = get_reviews(product_id)
            for r in reviews:
                print(f"- User {r['userId']} rated {r['rating']}★: {r['comment']}")

        elif choice == "5":
            result = get_avg_rating(product_id)
            print(f"\n📊 Product {product_id}:")
            print(f"⭐ Average Rating: {round(result['avgRating'], 2)}")
            print(f"🗳️ Total Reviews: {result['reviewCount']}")

        elif choice == "b":
            return
        else:
            print("Invalid choice.")

def show_cart():
    cart_items = get_cart(USER_ID)
    if not cart_items:
        print("🛒 Cart is empty.")
        return

    while True:
        print_line()
        print("YOUR CART:")
        for idx, item in enumerate(cart_items, 1):
            print(f"{idx}. Product ID: {item['productId']} | Quantity: {item['quantity']}")
        print("D. Delete an item from cart")
        print("B. Back to previous menu")
        print_line()
        choice = input("Choose an option: ").strip().lower()

        if choice == "b":
            return
        elif choice == "d":
            pid = input("Enter Product ID to remove: ").strip()
            if pid.isdigit():
                remove_from_cart(USER_ID, int(pid))
                cart_items = get_cart(USER_ID)  # refresh cart
            else:
                print("Invalid product ID.")
        else:
            print("Invalid choice.")

def main_menu():
    global USER_ID
    print_line()
    while True:
        try:
            USER_ID = int(input("Enter your User ID: ").strip())
            break
        except ValueError:
            print("Please enter a valid numeric User ID.")
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
