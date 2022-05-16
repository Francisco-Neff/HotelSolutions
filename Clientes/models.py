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
        
    def comprobarCliente(nombre,apellido,email):
    #Si el cliente enviado no existe se crea uno nuevo, para esto seria bueno añadir un nuevo campo de temporal en BBDD para eliminar estos registros
    #pasado el tiempo de la estancia
        id_cliente = Cliente.objects.filter(email = email)
        if not id_cliente:
            #Si no existe se crea un nuevo cliente.
            id_cliente , cliente = Cliente.definePkCliente(nombre,apellido,email)
            if id_cliente != 1 :
                cliente.save()
        else:
            #Si existe se obtiene la clave cliente.
            id_cliente=getattr(id_cliente[0],'id_cliente')
        return id_cliente

        