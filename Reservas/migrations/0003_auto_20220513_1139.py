# Generated by Django 3.1.1 on 2022-05-13 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reservas', '0002_auto_20220512_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='precio',
            name='cuantia',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
    ]