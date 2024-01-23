# Generated by Django 5.0.1 on 2024-01-14 16:32

import django.db.models.deletion
import product.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('start_year', models.IntegerField()),
                ('end_year', models.IntegerField()),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, upload_to=product.models.generate_unique_filename)),
                ('slug', models.SlugField(editable=False, max_length=255, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Vendor',
                'verbose_name_plural': 'Vendors',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(editable=False, max_length=255, unique=True)),
                ('description', models.TextField(blank=True)),
                ('description2', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to=product.models.generate_unique_filename)),
                ('has_offer', models.BooleanField(default=False)),
                ('is_featured', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('additional_description', models.TextField(blank=True)),
                ('slug', models.SlugField(editable=False, max_length=255, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('bikes', models.ManyToManyField(blank=True, related_name='products', to='product.bike')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.category')),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.vendor')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=product.models.generate_unique_filename)),
                ('alt_text', models.CharField(blank=True, max_length=255)),
                ('is_featured', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant_details', models.TextField(blank=True)),
                ('size', models.CharField(blank=True, max_length=255, null=True)),
                ('color', models.CharField(blank=True, max_length=255, null=True)),
                ('sku', models.CharField(max_length=255, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.PositiveIntegerField(default=0)),
                ('has_offer', models.BooleanField(default=False)),
                ('offer_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='variations', to='product.product')),
            ],
            options={
                'verbose_name': 'Variation',
                'verbose_name_plural': 'Variations',
            },
        ),
    ]
