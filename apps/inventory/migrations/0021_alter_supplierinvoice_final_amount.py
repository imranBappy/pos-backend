# Generated by Django 5.1.3 on 2025-03-05 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0020_alter_purchaseinvoiceitem_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplierinvoice',
            name='final_amount',
            field=models.DecimalField(decimal_places=8, default=0, max_digits=15),
        ),
    ]
