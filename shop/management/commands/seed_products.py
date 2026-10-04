from django.core.management.base import BaseCommand
from shop.models import Product


PRODUCTS = [
    {
        "name": "Wireless Headphones",
        "category": "Electronics",
        "description": "Comfortable over-ear wireless headphones with clear sound and long battery life.",
        "price": "2499.00",
        "stock": 25,
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Smart Watch",
        "category": "Electronics",
        "description": "A modern smartwatch for notifications, fitness tracking and everyday use.",
        "price": "3999.00",
        "stock": 18,
        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Classic Sneakers",
        "category": "Fashion",
        "description": "Lightweight everyday sneakers designed for comfort and casual style.",
        "price": "2199.00",
        "stock": 30,
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Minimal Backpack",
        "category": "Accessories",
        "description": "A practical backpack with a clean design and compartments for daily essentials.",
        "price": "1599.00",
        "stock": 22,
        "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Desk Lamp",
        "category": "Home",
        "description": "A compact desk lamp for study and work spaces with a warm modern look.",
        "price": "999.00",
        "stock": 35,
        "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Cotton Hoodie",
        "category": "Fashion",
        "description": "Soft cotton hoodie suitable for everyday wear and cooler evenings.",
        "price": "1799.00",
        "stock": 20,
        "image_url": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?auto=format&fit=crop&w=900&q=80",
    },
]


class Command(BaseCommand):
    help = "Create sample products for the e-commerce store."

    def handle(self, *args, **options):
        created = 0
        for data in PRODUCTS:
            product, was_created = Product.objects.get_or_create(
                name=data["name"],
                defaults=data,
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Sample product setup complete. {created} new products added."
        ))
