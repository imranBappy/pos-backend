from django.db import models
from apps.accounts.models import  User


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
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.id} - {self.name}"

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15, null=True, blank=True)
    email_address = models.EmailField(unique=True)
    address = models.TextField(null=True, blank=True)
    contact_person = models.CharField(max_length=100)
    branch =  models.CharField(max_length=100, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.id} - {self.name}"



class SupplierInvoice(models.Model):    
    due = models.DecimalField(max_digits=15, decimal_places=8 , null=True, blank=True, default=0)
    due_payment_date = models.DateField(null=True, blank=True)
    invoice_number = models.CharField(max_length=50, unique=True)
    po_number = models.CharField(max_length=50, unique=True, null=True, blank=True)

    final_amount = models.DecimalField(max_digits=15, decimal_places=8, default=0) # order amount 
    amount = models.DecimalField(max_digits=15, decimal_places=8, default=0)
    paid_amount  = models.DecimalField(max_digits=15, decimal_places=8, default=0)
    status = models.CharField(max_length=100, choices=PURCHASE_STATUS_CHOICES)
    supplier = models.ForeignKey(Supplier,on_delete=models.SET , null=True, blank=True, related_name='orders') # one to many
    invoice_image = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.id} - {self.status} - {self.amount} - {self.invoice_number}"
    class Meta:
        ordering = ['-created_at']  

class SupplierPayment(models.Model):
    invoice = models.ForeignKey(SupplierInvoice, on_delete=models.CASCADE, related_name="payments", null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[
        ('CASH', 'Cash'),
        ('BANK TRANSFER', 'Bank Transfer'),
        ('CHEQUE', 'Cheque'),
        ('CARD', 'Card'),
    ])
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
        return f"Payment of {self.amount}  for Invoice {self.invoice.invoice_number if self.invoice else 'N/A'}"
    class Meta:
        ordering = ['-created_at']  
    
class ItemCategory(models.Model):
    image = models.CharField(max_length=250, null=True, blank=True)
    name = models.CharField(max_length=100,  unique=True)
    description = models.TextField(max_length=100, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.id} - {self.name}"
    class Meta:
        ordering = ['-created_at']  



class Item(models.Model):
    name = models.CharField(max_length=100)    
    category = models.ForeignKey(ItemCategory, related_name='items', on_delete=models.SET_NULL, null=True, blank=True )
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='items' )
    safety_stock = models.IntegerField(default=0)
    sku = models.CharField(max_length=100, unique=True)
    stock = models.DecimalField(max_digits=14, decimal_places=8, default=0)
    current_stock = models.DecimalField(max_digits=14, decimal_places=8, default=0)

    image = models.TextField(blank=True, null=True, default="")
    vat = models.FloatField(default=0.0)
    
    @property
    def stock_level(self):
        if self.safety_stock == 0:
            return float('inf') if self.current_stock > 0 else 0

        return self.current_stock / self.safety_stock

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.name}"
    class Meta:
        ordering = ['-created_at']  

class PurchaseInvoiceItem(models.Model):
    """
        Purchase Item
    """
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='purchase_items')
    quantity =  models.DecimalField(max_digits=12, decimal_places=8, default=0)   
    total_quantity = models.DecimalField(max_digits=12, decimal_places=8, default=0)   
    supplier_Invoice = models.ForeignKey(SupplierInvoice, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchase_items')
    price =  models.DecimalField(max_digits=14, decimal_places=8) 
    vat = models.DecimalField(max_digits=12, decimal_places=8, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.id} - quantity: {self.quantity} - total_quantity: {self.total_quantity} - item: {self.item.name} - supplier_Invoice: {self.supplier_Invoice.invoice_number}"
    
    class Meta:
        ordering = ['-created_at']  



class WasteCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Example: Expired, Leftovers, Spoiled
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name



class Waste(models.Model):
    date = models.DateField()
    category = models.ForeignKey(WasteCategory, on_delete=models.CASCADE, related_name='wasted_ingredients')
    invoice = models.ForeignKey(SupplierInvoice, on_delete=models.SET_NULL, null=True, blank=True, related_name='wasted_ingredients')
    responsible = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='wasted_ingredients', null=True,  blank=True) 

    estimated_cost  = models.DecimalField(max_digits=12, decimal_places=8) 
    notes = models.TextField(null=True, blank=True)
  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    

    def __str__(self):
        return f"{self.id} -   "
    class Meta:
        ordering = ['-created_at']  

class WasteItem(models.Model):
    waste = models.ForeignKey(Waste,on_delete=models.CASCADE, related_name='waste_ingredient')
    ingredient = models.ForeignKey(Item,on_delete=models.CASCADE, related_name='waste_ingredient')
    quantity =  models.CharField(max_length=100)    
    loss_amount = models.DecimalField(max_digits=14, decimal_places=8)   
    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.ingredient.name}"
    class Meta:
        ordering = ['-created_at']  


class InvoiceConsumption(models.Model):
    order_ingredients_consumption = models.ForeignKey("product.OrderIngredients", on_delete=models.CASCADE, blank=True, null=True)
    waste_item = models.ForeignKey(WasteItem, on_delete=models.CASCADE, blank=True, null=True)
    purchase_invoice_item = models.ForeignKey(PurchaseInvoiceItem, on_delete=models.CASCADE)
    quantity =  models.DecimalField(max_digits=12, decimal_places=8, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.id}"
    class Meta:
        ordering = ['-created_at']