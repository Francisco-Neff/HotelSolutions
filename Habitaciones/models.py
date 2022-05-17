from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Habitacion(models.Model):
    class TipoHabitacion_Posibilidades(models.TextChoices):
        Individual= '1','Individual'
        Doble = '2','Doble'
        Triple = '3','Triple'
        Cuadruple = '4','Cuadruples'
    #Se podría definir el número de habitación como clave primaria, pero no seria una buena practica.
    id_habitacion = models.CharField(max_length=6,primary_key=True)
    tipo_habitacion = models.CharField(max_length=1, choices=TipoHabitacion_Posibilidades.choices,null=False)
    n_habitacion = models.SmallIntegerField(validators=[MaxValueValidator(999),MinValueValidator(1)], null=False)
    imagen = models.ImageField(upload_to ='static/img/habitaciones/')
    
    class DefinePkHab:
        #generación de la clave primaria de habitaciones siendo esta.
        # las 2 primeras posiciones fijas = HA. 
        # la 3 posición el tipo de habitación (1=inv, 2= dobles, 3= triples, 4=cuadru).
        # las 3 ultimas posiciones Nº de la Habitación rellenando con 0 a izquierda.
        def definePkHab(tipo_habitacion,n_habitacion):
            n_habitacion = '{:>03}'.format(n_habitacion)
            pk_habitacion = 'HA' + tipo_habitacion + n_habitacion
            if pk_habitacion in Habitacion.objects.values_list('id_habitacion', flat=True):
                pk_habitacion=1
            return pk_habitacion

    class UpdateHabitacion:
        #Para no perder la información que compone la clave primaria por lo que se identifica a simple vista el,
        #tipo de habitación y el número de esta, se procederá a hacer un delete del registro a actualizar, pero 
        #con las modificaiones enviadas. 
        def updateHabitacion(clave,tipo_habitacion,n_habitacion):
            upt = Habitacion.objects.get(id_habitacion=clave)
            alta = Habitacion.DefinePkHab.definePkHab(tipo_habitacion,n_habitacion)
            if alta!=1 : 
                upt.delete()
            return alta



    class Meta:
        verbose_name='Habitación'
        verbose_name_plural='Habitaciones'