import requests

API_BASE_URL = "http://localhost:5000/api"

def print_line():
    print("-" * 40)

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
            show_product_details(product['ProductID'])
        else:
            print("Invalid choice.")

def show_product_details(product_id):
    product = fetch_product_details(product_id)
    if not product:
        print("Product not found.")
        return

    print_line()
    print(f"PRODUCT DETAILS")
    print(f"Name: {product['Name']}")
    print(f"Price: {product['Price']} DKK")
    print(f"Stock: {product['Stock']}")
    print(f"Category ID: {product['CategoryID']}")
    print_line()
    input("Press Enter to go back...")

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
