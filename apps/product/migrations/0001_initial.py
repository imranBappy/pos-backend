# Generated by Django 5.1.3 on 2025-02-13 10:24

import datetime
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0001_initial'),
        ('kitchen', '0001_initial'),
        ('outlet', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('image', models.URLField(blank=True, default='')),
                ('description', models.TextField(blank=True, default='')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='product.category')),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('discount_type', models.CharField(choices=[('Flat', 'Flat'), ('Percentage', 'Percentage')], max_length=50)),
                ('discount_value', models.DecimalField(decimal_places=8, max_digits=12)),
                ('max_discount', models.DecimalField(blank=True, decimal_places=8, max_digits=12, null=True)),
                ('min_order_value', models.DecimalField(blank=True, decimal_places=8, max_digits=12, null=True)),
                ('valid_from', models.DateTimeField()),
                ('valid_until', models.DateTimeField()),
                ('usage_limit', models.IntegerField(default=0)),
                ('times_used', models.IntegerField(default=0)),
                ('per_user_limit', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('outlet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='coupons', to='outlet.outlet')),
            ],
        ),
        migrations.CreateModel(
            name='FloorTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('is_booked', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('floor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='floor_tables', to='product.floor')),
            ],
            options={
                'verbose_name': 'Floor Table',
                'verbose_name_plural': 'Floor Tables',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('DELIVERY', 'Delivery'), ('PICKUP', 'Pickup'), ('DINE_IN', 'Dine In')], max_length=100)),
                ('final_amount', models.DecimalField(decimal_places=8, default=0, max_digits=12)),
                ('amount', models.DecimalField(decimal_places=8, max_digits=12)),
                ('due', models.DecimalField(blank=True, decimal_places=8, default=0, max_digits=12, null=True)),
                ('due_payment_date', models.DateField(blank=True, null=True)),
                ('discount_applied', models.DecimalField(blank=True, decimal_places=8, max_digits=12, null=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled'), ('DUE', 'Due')], max_length=100)),
                ('order_id', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('is_cart', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='product.coupon')),
                ('outlet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='outlet.outlet')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='OrderReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, '⭐☆☆☆☆ (Poor)'), (2, '⭐⭐☆☆☆ (Fair)'), (3, '⭐⭐⭐☆☆ (Good)'), (4, '⭐⭐⭐⭐☆ (Very Good)'), (5, '⭐⭐⭐⭐⭐ (Excellent)')])),
                ('review_text', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='product.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_time', models.DateTimeField(blank=True, null=True)),
                ('additional_notes', models.TextField(blank=True, null=True)),
                ('floor_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_tables', to='product.floortable')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_tables', to='product.order')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=8, max_digits=12)),
                ('payment_method', models.CharField(choices=[('CASH', 'Cash'), ('CARD', 'Card')], max_length=100)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed'), ('FAILED', 'Failed'), ('REFUNDED', 'REFUNDED')], default='PENDING', max_length=100)),
                ('trx_id', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments', to='product.order')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments', to='inventory.supplier')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=8, max_digits=12)),
                ('description', models.TextField(blank=True, null=True)),
                ('images', models.TextField(blank=True, default='[]', null=True)),
                ('vat', models.FloatField(default=0.0)),
                ('sku', models.CharField(max_length=100)),
                ('cooking_time', models.CharField(blank=True, max_length=100, null=True)),
                ('video', models.TextField(blank=True, null=True)),
                ('tag', models.CharField(blank=True, choices=[('TOP_RATED', 'Top Rated'), ('RECOMMENDED', 'Recommended'), ('NEWLY_LAUNCHED', 'Newly Launched'), ('DAILY_SPECIAL', 'Daily Special'), ('HOT', 'Hot'), ('TRENDING', 'Trending'), ('BEST_SELLER', 'Best Seller'), ('POPULAR', 'Popular'), ('FEATURED', 'Featured')], max_length=50, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='product.category')),
                ('kitchen', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='kitchen.kitchen')),
                ('subcategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subcategory_products', to='product.category')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=8, max_digits=12)),
                ('vat', models.DecimalField(decimal_places=8, default=0, max_digits=12)),
                ('discount', models.DecimalField(decimal_places=8, default=0, max_digits=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='product.order')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ingredients', to='inventory.item')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='ExtraFood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=8, max_digits=12)),
                ('cooking_time', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extra_foods', to='product.product')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TableBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('duration', models.DurationField(default=datetime.timedelta(seconds=3600))),
                ('is_active', models.BooleanField(default=True)),
                ('floor_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='table_bookings', to='product.floortable')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='table_bookings', to='product.order')),
            ],
            options={
                'verbose_name': 'Table Booking',
                'verbose_name_plural': 'Table Bookings',
            },
        ),
        migrations.AddConstraint(
            model_name='floortable',
            constraint=models.UniqueConstraint(fields=('name', 'floor'), name='unique_table_name_per_floor_name'),
        ),
    ]
