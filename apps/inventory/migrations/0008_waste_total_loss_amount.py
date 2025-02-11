# Generated by Django 5.1.3 on 2025-02-09 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_alter_item_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='waste',
            name='total_loss_amount',
            field=models.DecimalField(decimal_places=8, default=0, max_digits=12),
            preserve_default=False,
        ),
    ]
