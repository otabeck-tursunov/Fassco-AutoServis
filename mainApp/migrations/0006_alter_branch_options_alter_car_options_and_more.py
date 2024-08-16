# Generated by Django 5.0.7 on 2024-08-15 16:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0005_product_min_amount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='branch',
            options={'verbose_name': 'Branch', 'verbose_name_plural': 'Branchs'},
        ),
        migrations.AlterModelOptions(
            name='car',
            options={'verbose_name': 'Car', 'verbose_name_plural': 'Cars'},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': 'Customer', 'verbose_name_plural': 'Customers'},
        ),
        migrations.AlterModelOptions(
            name='importproduct',
            options={'verbose_name': 'Import product', 'verbose_name_plural': 'Import products'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AlterModelOptions(
            name='provider',
            options={'verbose_name': 'Provider', 'verbose_name_plural': 'Providers'},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'verbose_name': 'Service', 'verbose_name_plural': 'Services'},
        ),
        migrations.AlterField(
            model_name='branch',
            name='address',
            field=models.TextField(blank=True, null=True, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='phone_number',
            field=models.CharField(blank=True, max_length=13, null=True, verbose_name='Phone number'),
        ),
        migrations.AlterField(
            model_name='car',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.branch', verbose_name='Branch'),
        ),
        migrations.AlterField(
            model_name='car',
            name='brand',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Brand'),
        ),
        migrations.AlterField(
            model_name='car',
            name='code',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='car',
            name='color',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Color'),
        ),
        migrations.AlterField(
            model_name='car',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='car',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.customer', verbose_name='Customer'),
        ),
        migrations.AlterField(
            model_name='car',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='car',
            name='state_number',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='State number'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.TextField(blank=True, null=True, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.branch', verbose_name='Branch'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='debt',
            field=models.FloatField(default=0, verbose_name='Debt'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='first_name',
            field=models.CharField(max_length=255, verbose_name='First name'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='last_name',
            field=models.CharField(max_length=255, verbose_name='Last name'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='passport_serial_letters',
            field=models.CharField(blank=True, max_length=7, null=True, verbose_name='Passport serial letters'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='passport_serial_numbers',
            field=models.CharField(blank=True, max_length=2, null=True, verbose_name='Passport serial numbers'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(blank=True, max_length=13, null=True, verbose_name='Phone number'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number_extra',
            field=models.CharField(blank=True, max_length=13, null=True, verbose_name='Phone number'),
        ),
        migrations.AlterField(
            model_name='importproduct',
            name='amount',
            field=models.FloatField(default=0, verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='importproduct',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.branch', verbose_name='Branch'),
        ),
        migrations.AlterField(
            model_name='importproduct',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='importproduct',
            name='debt',
            field=models.FloatField(default=0, verbose_name='Debt'),
        ),
        migrations.AlterField(
            model_name='importproduct',
            name='import_price',
            field=models.FloatField(blank=True, null=True, verbose_name='Import price'),
        ),
        migrations.AlterField(
            model_name='importproduct',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainApp.product', verbose_name='Product'),
        ),
        migrations.AlterField(
            model_name='importproduct',
            name='provider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainApp.provider', verbose_name='Provider'),
        ),
        migrations.AlterField(
            model_name='importproduct',
            name='total',
            field=models.FloatField(default=0, verbose_name='Total'),
        ),
        migrations.AlterField(
            model_name='product',
            name='amount',
            field=models.FloatField(default=0, verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='product',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.branch', verbose_name='Branch'),
        ),
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='product',
            name='export_price',
            field=models.FloatField(blank=True, null=True, verbose_name='Export price'),
        ),
        migrations.AlterField(
            model_name='product',
            name='import_price',
            field=models.FloatField(verbose_name='Import price'),
        ),
        migrations.AlterField(
            model_name='product',
            name='max_discount',
            field=models.FloatField(default=0, verbose_name='Max discount'),
        ),
        migrations.AlterField(
            model_name='product',
            name='min_amount',
            field=models.FloatField(default=10, verbose_name='Minimum amount'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='provider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainApp.provider', verbose_name='Provider'),
        ),
        migrations.AlterField(
            model_name='product',
            name='unit',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Unit'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.branch', verbose_name='Branch'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='debt',
            field=models.FloatField(default=0, verbose_name='Debt'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='phone_number',
            field=models.CharField(blank=True, max_length=13, null=True, verbose_name='Phone number'),
        ),
        migrations.AlterField(
            model_name='service',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.branch', verbose_name='Branch'),
        ),
        migrations.AlterField(
            model_name='service',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='service',
            name='price',
            field=models.FloatField(verbose_name='Price'),
        ),
    ]