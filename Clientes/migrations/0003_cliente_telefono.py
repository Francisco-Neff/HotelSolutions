# Generated by Django 3.1.1 on 2022-05-18 16:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clientes', '0002_auto_20220516_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='telefono',
            field=models.IntegerField(default=612345678, validators=[django.core.validators.MinValueValidator(600000000), django.core.validators.MaxValueValidator(700000000)]),
        ),
    ]
