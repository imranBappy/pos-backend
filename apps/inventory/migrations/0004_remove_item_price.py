# Generated by Django 5.1.3 on 2025-02-12 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_alter_supplierinvoice_amount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='price',
        ),
    ]
