# Generated by Django 5.0.7 on 2024-08-31 02:29

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0001_initial'),
        ('userApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='balance',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Balance'),
        ),
        migrations.AlterField(
            model_name='user',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainApp.branch', verbose_name='Branch'),
        ),
        migrations.AlterField(
            model_name='user',
            name='part',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Part'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=13, null=True, verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='user',
            name='position',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Position'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('SuperStatus', 'SuperStatus'), ('Manager', 'Manager'), ('Staff', 'Staff'), ('Worker', 'Worker')], default='Staff', max_length=50, verbose_name='Role'),
        ),
    ]