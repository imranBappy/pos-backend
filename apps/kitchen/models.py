from django.db import models
from django.db.models import SET_NULL


# imported models
# from apps.item.models import Item
# from outlet.models import Outlet


class Kitchen(models.Model):
    name = models.CharField(max_length=100, unique=True)
    photo = models.URLField()
    description = models.TextField()
    outlet = models.ForeignKey(
        "outlet.Outlet", on_delete=models.CASCADE, related_name="kitchens"
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id} - {self.name}"
    

class KitchenOrder(models.Model):
    KITCHEN_ORDER_STATUS = [
        ("PENDING", "Pending"),
        ("ACKNOWLEDGED", "Acknowledged"),
        ("IN_PROGRESS", "In Progress"),
        ("ON_HOLD", "On Hold"),
        ("READY", "Ready for Serving"),
        ("SERVED", "Served/Delivered"),
        ("CANCELLED", "Cancelled"),
    ]
    # order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='kitchen_orders')
    item = models.ForeignKey(
        "product.Product",
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="kitchen_orders",
    )
    status = models.CharField(
        max_length=20, choices=KITCHEN_ORDER_STATUS, default="PENDING"
    )
    # assigned_to = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
    kitchen = models.ForeignKey(
        Kitchen,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="kitchen_orders",
    )

    def __str__(self):
        return f"{self.id} - {self.status}"


class Printer(models.Model):
    name = models.CharField(max_length=100)
    kitchen = models.ForeignKey(
        Kitchen, on_delete=SET_NULL, null=True, blank=True, related_name="printers"
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id} - {self.name}"
