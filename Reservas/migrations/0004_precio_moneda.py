# Generated by Django 3.1.1 on 2022-05-17 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reservas', '0003_auto_20220513_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='precio',
            name='moneda',
            field=models.CharField(choices=[('€', 'Euro'), ('$', 'Dólar Americano'), ('£', 'Libra Esterlina')], default='€', max_length=1),
        ),
    ]
