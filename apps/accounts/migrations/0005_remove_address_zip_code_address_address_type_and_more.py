# Generated by Django 5.1.3 on 2025-01-17 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_building'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='zip_code',
        ),
        migrations.AddField(
            model_name='address',
            name='address_type',
            field=models.CharField(choices=[('HOME', 'Home'), ('OFFICE', 'Office')], default='HOME', max_length=10),
        ),
        migrations.AddField(
            model_name='address',
            name='default',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
