from unicodedata import decimal
from django.db import models
from Clientes import models as Clientes
from Habitaciones import models as Habitaciones

# Create your models here.
class Precio(models.Model):
    tipo_habitación = models.CharField(max_length=1, choices=Habitaciones.Habitacion.TipoHabitacion_Posibilidades.choices, null=False)
    cuantia = models.SmallIntegerField(null=False)
    class Meta:
        verbose_name='Precio'

class Reserva(models.Model):
    localizador = models.CharField(max_length=25,primary_key=True)
    id_habitacion = models.ForeignKey(Habitaciones.Habitacion,on_delete=models.CASCADE)
    id_cliente = models.ForeignKey(Clientes.Cliente,on_delete=models.CASCADE)
    fx_entrada = models.DateField(null=False)
    fx_salida = models.DateField(null=False)
    cuantia_total = models.DecimalField(max_digits=15,decimal_places=2,null=False)
        