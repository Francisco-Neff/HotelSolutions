from django.db import models

# Create your models here.

class Habitacion(models.Model):
    class TipoHabitacion_Posibilidades(models.TextChoices):
        Individual= '1','Individual'
        Doble = '2','Doble'
        Triple = '3','Triple'
        Cuadruple = '4','Cuadruples'
    #Se podría definir el número de habitación como clave primaria, pero no seria una buena practica.
    id_habitacion = models.CharField(max_length=6,primary_key=True)
    tipo_habitación = models.CharField(max_length=1, choices=TipoHabitacion_Posibilidades.choices,null=False)
    n_habitacion = models.SmallIntegerField(null=False)

    class Meta:
        verbose_name='Habitación'
        verbose_name_plural='Habitaciones'