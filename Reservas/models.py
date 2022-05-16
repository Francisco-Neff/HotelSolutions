from unicodedata import decimal
from django.db import models
from Clientes import models as Clientes
from Habitaciones import models as Habitaciones
import random
import string



# Create your models here.
class Precio(models.Model):
    tipo_habitación = models.CharField(max_length=1, choices=Habitaciones.Habitacion.TipoHabitacion_Posibilidades.choices, null=False)
    cuantia = models.DecimalField(max_digits=15,decimal_places=2,null=False)
    class Meta:
        verbose_name='Precio'
    def calcularPrecio(dias,id_habitacion):
        habitacion =  Habitaciones.Habitacion.objects.get(id_habitacion=id_habitacion)
        precio = Precio.objects.get(tipo_habitación=getattr(habitacion,'tipo_habitación'))
        return (float(getattr(precio,'cuantia'))* dias)
    

class Reserva(models.Model):
    localizador = models.CharField(max_length=25,primary_key=True)
    id_habitacion = models.ForeignKey(Habitaciones.Habitacion,on_delete=models.CASCADE)
    id_cliente = models.ForeignKey(Clientes.Cliente,on_delete=models.CASCADE)
    fx_entrada = models.DateField(null=False)
    fx_salida = models.DateField(null=False)
    cuantia_total = models.DecimalField(max_digits=15,decimal_places=2,null=False)
    class Meta:
        verbose_name='Reserva'
        verbose_name_plural='Reservas'    

    #Para definir el localizador de la reserva utilizaremos:
    #Primera posición fija con una 'R'. 
    #Segunda posición fija con el tipo de habitación contratada.
    #Posiciones de la 3 a la 10 con un random alfa numérico.
    def defineLocalizador(tipo_habitacion):
        localizador = 'R' + tipo_habitacion
        localizador = ''.join(random.sample(string.ascii_letters + string.digits, 7))
        return localizador

        

       

