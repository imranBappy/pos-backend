# Generated by Django 5.1.3 on 2025-02-19 03:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_parchageinvoiceitem_vat_supplierinvoice_final_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='alert_stock',
            new_name='safety_stock',
        ),
    ]
