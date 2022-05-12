from time import time
from django.shortcuts import render
from django.views import View
from .forms import DisponibilidadForm
from .models import Habitaciones,Reserva,Precio
from datetime import datetime,timedelta
from collections import defaultdict

# Create your views here.
class comprobarDisponibilidad(View):
    template_name='index.html'
    def get(self, request,*args, **kwargs):
        form = DisponibilidadForm()
        context={'form':form}
        return render(request,self.template_name,context)
    def post(self, request,*args, **kwargs):
        print('post',request.POST.get('fx_entrada'),'sal',request.POST.get('fx_salida'))
        fx_entrada=datetime.strptime(request.POST.get('fx_entrada') , "%d/%m/%Y").strftime('%Y-%m-%d')
        fx_salida=datetime.strptime(request.POST.get('fx_salida') , "%d/%m/%Y").strftime('%Y-%m-%d')
        print(fx_entrada)
        form = DisponibilidadForm(request.POST)
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
        print(habitaciones_disponibles)
        tabla = self.tablaDisponibilidad(habitaciones_disponibles,fx_entrada,fx_salida)
        context={'form':'formulario correcto'}
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

        #Generamos la tabla final para presentar al cliente con todas las opciones disponibles.
        tabla_final = []
        for habitacion in habitaciones_disponibles: 
            tabla_final.append(getattr(habitacion,'id_habitacion'))
            tabla_final.append(getattr(habitacion,'tipo_habitación'))
            cuantia = precios[str(getattr(habitacion,'tipo_habitación'))] * num_dias
            tabla_final.append(cuantia)
        print (tabla_final)
        #TODO meter todo esto en un FORM y mostrarselo al cliente.

      



            