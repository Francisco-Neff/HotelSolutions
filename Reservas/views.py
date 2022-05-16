import json
from django.shortcuts import redirect, render
from django.views import View

from Clientes.form import crearClienteForm
from .forms import DisponibilidadForm
from .models import Habitaciones,Reserva,Precio, Clientes
from datetime import datetime,timedelta
from collections import defaultdict
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse

# Create your views here.
class comprobarDisponibilidad(View):
    template_name='index.html'
    
    def get(self, request,*args, **kwargs):
        form = DisponibilidadForm()
        context={'form':form}
        return render(request,self.template_name,context)
    def post(self, request,*args, **kwargs):
        
        fx_entrada=datetime.strptime(request.POST.get('fx_entrada') , "%d/%m/%Y").strftime('%Y-%m-%d')
        fx_salida=datetime.strptime(request.POST.get('fx_salida') , "%d/%m/%Y").strftime('%Y-%m-%d')
        
        
        #Discriminador, recoge todas las habitaciones ocupadas cumpliendo la condición de
        #la entrada del nuevo huesped coincide con la entrada o próximas entradas de huespedes --fx_entrada__gte = fx_entrada-- 
        #ademas de la entrada del nuevo huesped concurre durante el tiempo con próximos huespedes o la salida de estos --fx_entrada__lte=fx_salida--
        #Con esto obtenemos todas las habitaciones ocupadas en el rango de fechas proporcionado en la petición. 
        disp = Reserva.objects.filter(fx_entrada__gte = fx_entrada,fx_entrada__lte=fx_salida)
      
        reg = []
        for hab in disp:
            if hab != None: 
                reg.append(getattr( getattr(hab,'id_habitacion'),'id_habitacion'))

        # Esta no es la manera mas optima de obtener todos los registros ya que con consulta INNERJOIN se pueda realizar en un único acceso a BBDD
        # pero con mis conocimientos actuales es la única manera que conozco
        habitaciones_disponibles = Habitaciones.Habitacion.objects.filter(tipo_habitación__lte = request.POST.get('huespedes')).exclude(id_habitacion__in=reg)
        
        tabla= self.tablaDisponibilidad(habitaciones_disponibles,fx_entrada,fx_salida)
        if len(tabla) != 0:
            form = crearClienteForm()
            context={'habitaciones':tabla,'form':form,'fx_entrada':fx_entrada,'fx_salida':fx_salida }
            return render(request,'contratacion.html',context) 
            
        else:
            form = DisponibilidadForm()
            context={'error':'No se ha podido generar correctamente la disponibilidad de habitaciones, vuelva a intentarlo en otro momento', 
            'form':form}
            return render(request,self.template_name,context)

    def tablaDisponibilidad(self,habitaciones_disponibles,fx_entrada,fx_salida):
        #Calculamos el número de días que se hospeda el cliente.
        num_dias = (datetime.strptime(fx_salida,'%Y-%m-%d') - datetime.strptime(fx_entrada,'%Y-%m-%d'))/timedelta(days=1)

        #Convertimos el listado de tipo de habitación con precios en un diccionario para trabajar mejor con el y ahorrar consultas por 
        #cada habitación disponible
        precios_list = list(Precio.objects.values_list('tipo_habitación','cuantia'))
        precios = {}
        for hab,precio in precios_list:
            precios[hab] = precio

        #Generamos la tabla final para presentar al cliente con todas las opciones disponibles en formato JSON:
        #{habitacion: id_habitacion, huespedes: num_personas_max, precio: cuantia_total_estancia}
        tabla_final = []
        
        for habitacion in habitaciones_disponibles: 
            tupla={}
            tupla['habitacion']=getattr(habitacion,'id_habitacion')
            tupla['huespedes']=getattr(habitacion,'tipo_habitación')
            tupla['precio']= float(precios[str(getattr(habitacion,'tipo_habitación'))]) * num_dias
            tabla_final.append(tupla)
        data = json.dumps(tabla_final)      
        return data



def confirmarReserva(request):
    form = crearClienteForm(request.POST)
    
    if form.is_valid():
        print('valido')
        #Si el cliente enviado no existe se crea uno nuevo, para esto seria bueno añadir un nuevo campo de temporal en BBDD para eliminar estos registros
        #pasado el tiempo de la estancia
        pk_cliente = Clientes.Cliente.objects.filter(nombe = request.POST['nombre'], apellido = request.POST['apellido'], email = request.POST['email'])
        print('cliente',pk_cliente)
    else:
        msg='El email o nombre introducido no son correctos, por favor recuerde el @'
        print(msg)
    print(request)
    print('Post1',request.POST.get('id_habitacion'))
    print('Post1',request.POST)
    print('Post1',request.POST['nombre'])
    if request.POST['nombre'] == '':
        print(len(request.POST['nombre']))

    #print('Post1',request.POST['apellido'])
    #print('Post1',request.POST['email'])

    return render (request,'index.html')

      



            