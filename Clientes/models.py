from django.db import models
import random

# Create your models here.
class Cliente(models.Model):
    id_cliente = models.CharField(max_length=7,primary_key=True)
    nombre = models.CharField(max_length=50,null=False)
    apellido = models.CharField(max_length=50,null=False)
    email = models.EmailField(max_length=150,null=False,unique=True)
    class Meta:
        verbose_name='Cliente'
        verbose_name_plural='Clientes'

    
    #generación de la clave primaria de Cliente.
    # las 3 primeras posiciones fijas constaran de una 'C' y la incial de su nombre y apellido. 
    # la 4 siguientes posiciones sera un número random
    def definePkCliente(nombre,apellido,email):
        pk_cliente = 'C' + nombre[0] + apellido[0] +str(random.randint(1000, 9999))
        if pk_cliente in Cliente.objects.values_list('id_cliente', flat=True):
            pk_cliente=1
            cliente=None
        else:
            cliente = Cliente(id_cliente=pk_cliente,nombre=nombre,apellido=apellido,email=email)
        return pk_cliente, cliente

    #Update de los datos de un cliente
    def updateCliente(id_cliente,nombre,apellido,email):
        upt = Cliente.objects.get(id_cliente=id_cliente)
        upt.nombre = nombre
        upt.apellido = apellido
        upt.email = email
        upt.save()
        