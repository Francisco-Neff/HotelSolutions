from django.db import models

# Create your models here.
class Cliente(models.Model):
    id_cliente = models.CharField(max_length=7,primary_key=True)
    nombre = models.CharField(max_length=50,null=False)
    apellido = models.CharField(max_length=50,null=False)
    email = models.EmailField(max_length=150,null=False)
    class Meta:
        verbose_name='Cliente'
        verbose_name_plural='Clientes'