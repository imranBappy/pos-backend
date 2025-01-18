from django.db import models
from apps.accounts.models import User, Address
from apps.outlet.models import Outlet
from django.utils.timezone import now
from datetime import timedelta
import uuid
from django.utils import timezone

class Category(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE,  related_name='subcategories')
    name = models.CharField(max_length=100, unique=True)
    image = models.URLField(default="", blank=True)
    description = models.TextField(default="", blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
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
    price = models.DecimalField(max_digits=12, decimal_places=8)
    description = models.TextField(null=True, blank=True)
    images = models.TextField(blank=True, null=True, default="[]")
    tax = models.FloatField(default=0.0)
    sku = models.CharField(max_length=100)
    cooking_time = models.CharField(max_length=100, null=True, blank=True)
    video = models.TextField(null=True, blank=True)
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
    is_tax_included = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.name}"
    
    class Meta:
        ordering = ['-created_at']
        

# Extra some food with product. 
class ExtraFood(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="extra_foods")
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cooking_time = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.id} - {self.name}"
    
    class Meta:
        ordering = ['-created_at']

ORDER_TYPE_CHOICES = [
        ("DELIVERY", "Delivery"),
        ("PICKUP", "Pickup"),
        ("DINE_IN", "Dine In"),
    ]
    
ORDER_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled")
    ]
PAYMENT_METHOD_CHOICES = [
        ("CASH", "Cash"),
        ("CARD", "Card"),
        ('COMBINE', 'Combine')
    ]
class Floor(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    def __str__(self):
        return f"{self.id}-{self.name}"
    
class FloorTable(models.Model):
    name = models.CharField(max_length=100)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='floor_tables')
    is_active = models.BooleanField(default=True)
    is_booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    
    def __str__(self):
        return f"Table {self.name} on Floor {self.floor.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'floor'],
                name='unique_table_name_per_floor_name'
            )
        ]
        verbose_name = 'Floor Table'
        verbose_name_plural = 'Floor Tables'
        ordering = ['name']
     
class InvalidCouponError(Exception):
    pass   
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    DISCOUNT_TYPE_CHOOSE = [
        ('Flat', 'Flat'),
        ('Percentage', 'Percentage'),
    ]
    discount_type = models.CharField(max_length=50, choices=DISCOUNT_TYPE_CHOOSE)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2) # percentage or amount
    
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # The maximum amount a discount can provide when the coupon type is "Percentage."
    min_order_value = models.DecimalField(max_digits=10, decimal_places=2,  null=True, blank=True) # The minimum order amount required for the coupon to be valid.
    
    valid_from = models.DateTimeField()
    valid_until  = models.DateTimeField()
    usage_limit = models.IntegerField(default=0)
    times_used = models.IntegerField(default=0) # It increase by 1 one every time when it will used
    
    per_user_limit = models.IntegerField(default=0) # '0' No limit on the number of times a user can use it.
    
    outlet = models.ForeignKey(Outlet, on_delete=models.SET_NULL, null=True, blank=True, related_name="coupons")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def is_valid(self, amount, userId):
            
        # time validation
        if self.valid_from < timezone.now() or timezone.now() > self.valid_until:
            raise InvalidCouponError("Invalid coupon.")
        
        #  min_order_value validation
        if self.min_order_value and  (self.min_order_value > amount):
            raise InvalidCouponError(f"You have to buy minmum {self.min_order_value} of product")
        
        # usage_limit validation
        if self.usage_limit and  self.times_used >= self.usage_limit:
            raise InvalidCouponError(f"Invalid coupon.")
        
        if self.per_user_limit:
            order_count = Order.objects.filter(user=userId, coupon=self).count()
            if order_count >= self.per_user_limit:
                raise InvalidCouponError("Coupon usage limit exceeded for this user.")
        
        return 0
            
    
    def discount_amount(self, amount):
        if self.discount_type == self.DISCOUNT_TYPE_CHOOSE[0][0]:
            discount = self.discount_value
            return max(amount - discount, 0)
        elif  self.discount_type == self.DISCOUNT_TYPE_CHOOSE[1][0]:
            discount = (amount * self.discount_value) / 100
            if self.max_discount:
                discount = min(discount, self.max_discount)
            return max(amount - discount, 0)
        return amount
                
    def apply(self):
        self.times_used = F('times_used') + 1
        self.save(update_fields=['times_used'])           
    
    def __str__(self):
        return f"{self.id} - {self.code}"
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    type = models.CharField(max_length=100, choices=ORDER_TYPE_CHOICES)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True ,blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL,null=True ,blank=True, related_name='orders')
    discount_applied = models.DecimalField(max_digits=10, decimal_places=2 , null=True ,blank=True)
    
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES)
    outlet = models.ForeignKey(Outlet, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    order_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    is_cart = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if self.coupon:
            if self.coupon.is_valid(self.amount, self.user.id):
                discount = self.coupon.discount_amount(self.amount)
                self.discount_applied = self.amount - discount
                self.final_amount = self.final_amount - (self.amount - discount)
            else:
                raise ValueError("Invalid coupon.")
            self.coupon.apply()
        else:
            self.final_amount = self.final_amount
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.id}"
    
    class Meta:
        ordering = ['-id'] 

class OrderTable(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_tables")
    floor_table = models.ForeignKey(FloorTable, on_delete=models.CASCADE, related_name="order_tables")
    booking_time = models.DateTimeField(null=True, blank=True)  # Example additional field
    additional_notes = models.TextField(null=True, blank=True)  # Example additional field
    
class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='items') 
    
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    def __str__(self):
        return f"{self.id}"

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
        ("REFUNDED", "Refunded"),
    ]
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, related_name='payments', null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=100, 
        choices=PAYMENT_METHOD_CHOICES
    )
    status = models.CharField(
        max_length=100, 
        choices=PAYMENT_STATUS_CHOICES, 
        default="PENDING"
    )
    trx_id = models.CharField(
        max_length=100, 
        unique=True, 
        null=True, 
        blank=True
    )
    remarks = models.TextField(
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Payment {self.id} - Order {self.order.id} - Status {self.status}"

class TableBooking(models.Model):
    floor_table = models.ForeignKey(FloorTable, on_delete=models.CASCADE, related_name='table_bookings')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='table_bookings')
    start_time = models.DateTimeField(default=now)
    duration = models.DurationField(default=timedelta(hours=1))
    is_active = models.BooleanField(default=True)
    
    def end_time(self):
        return self.start_time + self.duration
    
    def __str__(self):
        return f"ID: {self.id} - { self.floor_table.name  } - Active: {self.is_active}"

    class Meta:
        verbose_name = "Table Booking"
        verbose_name_plural = "Table Bookings"
