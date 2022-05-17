import random
import string
from unicodedata import decimal
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from Clientes import models as Clientes
from Habitaciones import models as Habitaciones




# Create your models here.
class Precio(models.Model):
    class TipoMoneda_Posibilidades(models.TextChoices):
        #En un primer momento se define la moneda para todas en € por si en el futuro se implementa un conversor de precio según moneda.
        Euro= '€','Euro'
        Dolar_U = '$','Dólar Americano'
        Libra_E = '£','Libra Esterlina'
    tipo_habitacion = models.CharField(max_length=1, choices=Habitaciones.Habitacion.TipoHabitacion_Posibilidades.choices, null=False)
    cuantia = models.DecimalField(max_digits=15,decimal_places=2,null=False)
    moneda = models.CharField(max_length=1, choices=TipoMoneda_Posibilidades.choices,default=TipoMoneda_Posibilidades.Euro)
    class Meta:
        verbose_name='Precio'
    def calcularPrecio(dias,id_habitacion):
        habitacion =  Habitaciones.Habitacion.objects.get(id_habitacion=id_habitacion)
        precio = Precio.objects.get(tipo_habitacion=getattr(habitacion,'tipo_habitacion'))
        return (float(getattr(precio,'cuantia'))* dias)
    

class Reserva(models.Model):
    localizador = models.CharField(max_length=25,primary_key=True)
    id_habitacion = models.ForeignKey(Habitaciones.Habitacion,on_delete=models.CASCADE)
    id_cliente = models.ForeignKey(Clientes.Cliente,on_delete=models.CASCADE)
    fx_entrada = models.DateField(null=False)
    fx_salida = models.DateField(null=False)
    cuantia_total = models.DecimalField(max_digits=15,decimal_places=2,null=False)
    moneda = models.CharField(max_length=1, choices=Precio.TipoMoneda_Posibilidades.choices,default=Precio.TipoMoneda_Posibilidades.Euro)
    huespedes = models.SmallIntegerField(validators=[MaxValueValidator(4),MinValueValidator(1)])
    class Meta:
        verbose_name='Reserva'
        verbose_name_plural='Reservas'    

    #Para definir el localizador de la reserva utilizaremos:
    #Primera posición fija con una 'R'. 
    #De la 2 a la 6 posición fija con el id de habitación contratada.
    #Posiciones de la 3 a la 10 con un random alfa numérico.
    def defineLocalizador(id_habitacion):
        localizador = 'R' + id_habitacion
        localizador = localizador + ''.join(random.sample(string.ascii_letters + string.digits, 7))
        return localizador
    

    def mostrarReservas(tipo,clave):
        #Si el tipo es 1 se enviaran todas las reservas del cliente enviado en la clave
        #Si el tipo es 2 se enviaran todas las reservas de la habitacion enviada en la clave
        #Si el tipo es 3 se enviara la reserva asociada al localizador.
        if tipo == 1: #Clave Cliente
            registros = Reserva.objects.filter(id_cliente=clave)
        elif tipo == 2: #Clave Habitación
            registros = Reserva.objects.filter(id_habitacion=clave)
        for registro in registros:
            print(registro)
        return registros
        

       

