# Generated by Django 3.1.1 on 2022-05-17 16:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reservas', '0006_reserva_huespedes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='huespedes',
            field=models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(1)]),
        ),
    ]
