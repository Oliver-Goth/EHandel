from mongo_review_functions import add_review, get_avg_rating, get_reviews

def menu():
    print("\n📦 Review CLI Menu")
    print("1. ➕ Submit a review")
    print("2. 📝 View recent reviews")
    print("3. 📊 View average rating")
    print("4. ❌ Exit")

def cli():
    while True:
        menu()
        choice = input("\nSelect an option (1–4): ")

        if choice == "1":
            product_id = input("Enter Product ID (e.g. P001): ")
            user_name = input("Your name: ")
            rating = input("Rating (1–5): ")
            comment = input("Your review: ")
            add_review(product_id, user_name, rating, comment)

        elif choice == "2":
            product_id = input("Enter Product ID to view reviews: ")
            print(f"\nRecent reviews for {product_id}:")
            for r in get_reviews(product_id):
                print(f"- {r['userName']} rated {r['rating']}★: {r['comment']}")

        elif choice == "3":
            product_id = input("Enter Product ID to view rating: ")
            result = get_avg_rating(product_id)
            print(f"\n📊 Product {product_id}:")
            print(f"⭐ Average Rating: {round(result['avgRating'], 2)}")
            print(f"🗳️ Total Reviews: {result['reviewCount']}")

        elif choice == "4":
            print("👋 Exiting CLI.")
            break

        else:
            print("⚠️ Invalid choice. Try again.")

if __name__ == "__main__":
    cli()
