# Generated by Django 5.0.7 on 2024-08-09 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0004_importproduct_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='min_amount',
            field=models.FloatField(default=10),
        ),
    ]