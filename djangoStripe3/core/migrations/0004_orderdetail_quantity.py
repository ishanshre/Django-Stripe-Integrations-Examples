# Generated by Django 4.1.5 on 2023-01-19 03:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_orderdetail_has_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='quantity',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]