# Generated by Django 5.1.3 on 2025-03-06 01:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_alter_payment_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderingredients',
            name='order_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_ingredients', to='product.orderproduct'),
        ),
    ]
