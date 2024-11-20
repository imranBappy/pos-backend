from django.db import models

# imported models
# from kitchen.models import Kitchen


# Create your models here.


class Category(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE,  related_name='subcategories')
    name = models.CharField(max_length=100, unique=True)
    photo = models.URLField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.id} - {self.name}"


class Product(models.Model):
    TAGS_CHOOSE = [
        ("TOP_RATED", "Top Rated"),
        ("RECOMMENDED", "Recommended"),
        ("NEWLY_LAUNCHED", "Newly Launched"),
        ("DAILY_SPECIAL", "Daily Special"),
        ("HOT", "Hot"),
        ("TRENDING", "Trending"),
        ("BEST_SELLER", "Best Seller"),
        ("POPULAR", "Popular"),
        ("FEATURED", "Featured")
    ]
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    photo = models.TextField(blank=True, null=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=100)
    cooking_time = models.TimeField(null=True, blank=True)
    tag = models.CharField(max_length=50, choices=TAGS_CHOOSE,
        null=True, blank=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="products"
    )
    subcategory = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True,
     related_name="subcategory_products"
    )
    kitchen = models.ForeignKey(
        "kitchen.Kitchen",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.id} - {self.name}"
