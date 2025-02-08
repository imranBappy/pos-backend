from faker import Faker
import random
from apps.product.models import Category, Product
from django.db import transaction
import json

fake = Faker()

# Constants
MAIN_CATEGORIES = [
    "Food", "Beverages", "Desserts", "Appetizers", "Main Course",
    "Breakfast", "Lunch", "Dinner", "Snacks", "Special Items",
]

SUB_CATEGORIES = {
    "Food": ["Pizza", "Burger", "Pasta", "Sandwich", "Rice Bowl"],
    "Beverages": ["Hot Drinks", "Cold Drinks", "Smoothies", "Juices", "Mocktails"],
    "Desserts": ["Ice Cream", "Cakes", "Puddings", "Pastries", "Cookies"],
    "Appetizers": ["Soups", "Salads", "Starters", "Finger Food", "Dips"],
    "Main Course": ["Indian", "Chinese", "Italian", "Mexican", "Thai"],
    "Breakfast": ["Continental", "American", "Indian", "Healthy", "Quick Bites"],
    "Lunch": ["Executive", "Light", "Heavy", "Combo", "Special"],
    "Dinner": ["Family", "Couple", "Group", "Party", "Regular"],
    "Snacks": ["Chips", "Nuts", "Fries", "Nachos", "Popcorn"],
    "Special Items": ["Chef's Special", "Seasonal", "Festival", "Weekend", "Limited Edition"],
}

TAGS = ["TOP_RATED", "RECOMMENDED", "NEWLY_LAUNCHED", "DAILY_SPECIAL", 
        "HOT", "TRENDING", "BEST_SELLER", "POPULAR", "FEATURED"]

@transaction.atomic
def create_fake_data():
    # Create main categories
    main_categories = {}
    for cat_name in MAIN_CATEGORIES:
        category = Category.objects.create(
            name=cat_name,
            image=fake.image_url(),
            description=fake.text(max_nb_chars=200),
            is_active=True
        )
        main_categories[cat_name] = category
        print(f"Created main category: {cat_name}")

    # Create subcategories
    sub_categories = []
    for main_cat, subs in SUB_CATEGORIES.items():
        for sub_name in subs:
            sub_category = Category.objects.create(
                name=f"{main_cat} - {sub_name}",
                parent=main_categories[main_cat],
                image=fake.image_url(),
                description=fake.text(max_nb_chars=200),
                is_active=True
            )
            sub_categories.append(sub_category)
            print(f"Created subcategory: {sub_name} under {main_cat}")

    # Create products
    products_created = 0
    for _ in range(10000):
        main_cat = random.choice(list(main_categories.values()))
        sub_cat = random.choice(Category.objects.filter(parent=main_cat))
        
        product = Product.objects.create(
            name=fake.unique.catch_phrase(),
            price=round(random.uniform(5.0, 500.0), 2),
            description=fake.text(max_nb_chars=300),
            images=json.dumps([fake.image_url() for _ in range(random.randint(1, 5))]),
            vat=round(random.uniform(0, 18), 2),
            sku=fake.unique.ean13(),
            cooking_time=f"{random.randint(5, 60)} minutes",
            video=fake.url() if random.random() > 0.7 else None,
            tag=random.choice(TAGS) if random.random() > 0.5 else None,
            category=main_cat,
            subcategory=sub_cat,
            is_active=random.choice([True, True, True, False])  # 75% chance of being active
        )
        products_created += 1
        if products_created % 100 == 0:
            print(f"Created {products_created} products")

    print("\nData creation completed:")
    print(f"Main Categories: {len(main_categories)}")
    print(f"Subcategories: {len(sub_categories)}")
    print(f"Products: {products_created}")

if __name__ == "__main__":
    # Clear existing data (optional)
    print("Clearing existing data...")
    Product.objects.all().delete()
    Category.objects.all().delete()
    
    print("Starting data creation...")
    create_fake_data()
