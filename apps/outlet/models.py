from django.db import models


# Create your models here.


class Outlet(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=250)
    # cashier  = models.OneToOneField("User", on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id} - {self.name}"
