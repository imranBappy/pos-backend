# Generated by Django 5.1.3 on 2025-03-04 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0018_alter_item_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseinvoiceitem',
            name='total_quantity',
            field=models.DecimalField(decimal_places=8, default=0, max_digits=12),
        ),
    ]
