from django.db import models
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
from apps.accounts.models import Address, User  # Adjust the import path as needed.
class PAYMENT_STATUS_CHOICES(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    COMPLETED = 'COMPLETED', 'Completed'
    FAILED = 'FAILED', 'Failed'
    REFUNDED = 'REFUNDED', 'REFUNDED'
class PURCHASE_STATUS_CHOICES(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    COMPLETED = 'COMPLETED', 'Completed'
    CANCELLED = 'CANCELLED', 'Cancelled'
    DUE = 'DUE', 'Due'

class Unit(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"{self.id} - {self.name}"

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15, null=True, blank=True)
    email_address = models.CharField(max_length=30, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.id} - {self.name}"

# # Need another model for saveing what will buy from this  supplier
# class Save(models.Model):

    
#     pass


class SupplierInvoice(models.Model):    
    due = models.DecimalField(max_digits=12, decimal_places=8 , null=True, blank=True, default=0)
    due_payment_date = models.DateField(null=True, blank=True)
    invoice_number = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=8, default=0)
    status = models.CharField(max_length=100, choices=PURCHASE_STATUS_CHOICES)
    supplier = models.ForeignKey(Supplier,on_delete=models.SET , null=True, blank=True, related_name='orders') # one to many
    invoice_image = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.id} - {self.status} - {self.amount}"
    # invoice_number, amount, images, items

class SupplierPayment(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="supplier_payments")
    invoice = models.ForeignKey(SupplierInvoice, on_delete=models.CASCADE, related_name="payments", null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[
        ('Cash', 'Cash'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Cheque', 'Cheque'),
    ])
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    trx_id = models.CharField(
        max_length=100,
        unique=True, 
        null=True, 
        blank=True
    )
    status = models.CharField(
        max_length=100, 
        choices=PAYMENT_STATUS_CHOICES, 
        default="PENDING"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Payment of {self.amount_paid}  for Invoice {self.invoice.invoice_number if self.invoice else 'N/A'}"
    
class ItemCategory(models.Model):
    image = models.CharField(max_length=250, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.id} - {self.name}"
   
class Item(models.Model):
    name = models.CharField(max_length=100)    
    category = models.ForeignKey(ItemCategory, related_name='items', on_delete=models.SET_NULL, null=True, blank=True )
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL,null=True, blank=True, related_name='ingredients' )
    alert_stock = models.IntegerField(default=0)
    sku = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=12, decimal_places=8)
    stock = models.IntegerField(default=0)
    current_stock = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.id} - {self.name}"

class ParchageInvoiceItem(models.Model):
    """
    Order Item
    """
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='parchage_items')
    quantity =  models.CharField(max_length=100)    
    supplier_parchange = models.ForeignKey(SupplierInvoice, on_delete=models.SET_NULL, null=True, blank=True, related_name='parchage_items')
    price =  models.DecimalField(max_digits=12, decimal_places=8) 
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.id} - {self.supplier.name}"
    
class Waste(models.Model):
    date = models.DateField()
    responsible = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='waste', null=True,  blank=True) 
    note = models.TextField(null=True, blank=True)
    total_loss_amount  = models.DecimalField(max_digits=12, decimal_places=8)   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.id} -  {self.responsible.name}"
    
class WasteItem(models.Model):
    waste = models.ForeignKey(Waste,on_delete=models.CASCADE, related_name='waste_ingredient')
    ingredient = models.ForeignKey(Item,on_delete=models.CASCADE, related_name='waste_ingredient')
    quantity =  models.CharField(max_length=100)    
    loss_amount = models.DecimalField(max_digits=12, decimal_places=8)   

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.ingredient.name}"


