# Generated by Django 5.1.3 on 2025-03-05 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0023_alter_purchaseinvoiceitem_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wasteitem',
            name='loss_amount',
            field=models.DecimalField(decimal_places=8, max_digits=14),
        ),
    ]
