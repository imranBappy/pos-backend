# Generated by Django 5.1.3 on 2025-02-08 03:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_alter_supplier_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='alert_quantity',
            new_name='alert_stock',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='current_stock',
            new_name='stock',
        ),
    ]
