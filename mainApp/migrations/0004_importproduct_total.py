# Generated by Django 5.0.7 on 2024-07-31 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0003_importproduct_import_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='importproduct',
            name='total',
            field=models.FloatField(default=0),
        ),
    ]