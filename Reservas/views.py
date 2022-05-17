import json
from datetime import datetime,timedelta,date
from django.shortcuts import  render
from django.views import View
from Clientes.form import crearClienteForm
from .forms import DisponibilidadForm,BuscarClaveForm
from .models import Habitaciones,Reserva,Precio, Clientes

FECHA_MAXIMA = '2022-12-31'

# Create your views here.
class comprobarDisponibilidad(View):
    template_name='nuevareserva.html'
    form = DisponibilidadForm()

    def get(self, request,*args, **kwargs):  
        context={'form':self.form}
        return render(request,self.template_name,context)

    def post(self, request,*args, **kwargs):        
        #Se valida que la fecha de salida no sea superior al 2022-12-31 
        #Se valida que la fecha de entrada no sea inferior al día actual
        #Se valida que la fecha de salida no sea inferior o igual a la de entrada
        fx_entrada=datetime.strptime(request.POST.get('fx_entrada') , "%d/%m/%Y")
        fx_salida=datetime.strptime(request.POST.get('fx_salida'), "%d/%m/%Y")
        if fx_salida > datetime(2022,12,31):
            context={'error':'No se puedes seleccionar una fecha maxima por encima de '+FECHA_MAXIMA,'form':self.form}
            return render(request,self.template_name,context)
        elif fx_entrada < datetime.strptime(datetime.today().strftime("%d/%m/%Y"), "%d/%m/%Y"):
            context={'error':'La fecha de entrada no puede ser menor a la de hoy','form':self.form}
            return render(request,self.template_name,context)
        elif fx_salida <= fx_entrada:
            context={'error':'La fecha de salida no puede ser menor o igual que la de entrada','form':self.form}
            return render(request,self.template_name,context)
        
        fx_entrada=fx_entrada.strftime('%Y-%m-%d')
        fx_salida=fx_salida.strftime('%Y-%m-%d')
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
        habitaciones_disponibles = Habitaciones.Habitacion.objects.filter(tipo_habitacion__lte = request.POST.get('huespedes')).exclude(id_habitacion__in=reg)
        tabla= self.tablaDisponibilidad(habitaciones_disponibles,fx_entrada,fx_salida)

        if len(tabla) != 0: 
            #Si tenemos registros de disponibilidad se los mostramos al cliente
            #Renderizamos una nueva vista con el formulario y datos necesarios para crear esta nueva vista.
            form = crearClienteForm()
            context={'habitaciones':tabla,'form':form,'fx_entrada':fx_entrada,'fx_salida':fx_salida,'huespedes':request.POST.get('huespedes') }
            return render(request,'contratacion.html',context)
            
        else: #Si no tenemos registros de disponibilidad se los comunicamos al cliente
            context={'error':'No se ha podido generar correctamente la disponibilidad de habitaciones, vuelva a intentarlo en otro momento', 
            'form':self.form}
            return render(request,self.template_name,context)

    def tablaDisponibilidad(self,habitaciones_disponibles,fx_entrada,fx_salida):
        #Calculamos el número de días que se hospeda el cliente.
        num_dias = (datetime.strptime(fx_salida,'%Y-%m-%d') - datetime.strptime(fx_entrada,'%Y-%m-%d'))/timedelta(days=1)

        #Convertimos el listado de tipo de habitación con precios en un diccionario para trabajar mejor con el y ahorrar consultas por 
        #cada habitación disponible
        precios_list = list(Precio.objects.values_list('tipo_habitacion','cuantia','moneda'))
        precios = {}
        for hab,precio,moneda in precios_list:
            precios[hab] = precio
            moneda=moneda
          
        #Generamos la tabla final para presentar al cliente con todas las opciones disponibles en formato JSON:
        #{habitacion: id_habitacion, huespedes: num_personas_max, precio: cuantia_total_estancia con moneda}
        # devolvemos esta tabla generada
        tabla_final = []
        for habitacion in habitaciones_disponibles: 
            tupla={}
            tupla['habitacion']=getattr(habitacion,'id_habitacion')
            tupla['huespedes']=getattr(habitacion,'tipo_habitacion')
            tupla['precio']= str(float(precios[str(getattr(habitacion,'tipo_habitacion'))]) * num_dias) + moneda
            tabla_final.append(tupla)
        data = json.dumps(tabla_final)      
        return data


class ConfirmarReserva(View):
    template_name='index.html'
    registros = Reserva.objects.filter(fx_salida__gte = date.today().strftime('%Y-%m-%d'))
    context={}
    context['registros']=registros
    def post(self, request,*args, **kwargs):
        #Vista para realizar la reserva con los datos enviados por el cliente
        #Solo se podrá llegar a esta vista con una petición POST

        id_cliente = Clientes.Cliente.comprobarCliente(request.POST['nombre'],request.POST['apellido'],request.POST['email'])
        if id_cliente != 1:
            #Una vez recibido el ID del cliente se realiza la verificación de la habitación no este reservada.
            fx_salida = request.POST['fx_salida']
            fx_entrada = request.POST['fx_entrada']

            #Antes de realizar el alta comprobamos que la habitación no haya sido ocupada en el transcurso.
            if not Reserva.objects.filter(id_habitacion = request.POST['id_habitacion'],fx_entrada__gte = fx_entrada ,fx_entrada__lte=fx_salida):
                #Volvemos a calcular el importe servidor para evitar la posible modificación de precios por clientes.
                dias = (datetime.strptime(fx_salida,'%Y-%m-%d') - datetime.strptime(fx_entrada,'%Y-%m-%d'))/timedelta(days=1)
                cuantia_total = Precio.calcularPrecio(dias,request.POST['id_habitacion'])

                #Se realiza la reserva.
                id_reserva = Reserva.defineLocalizador(request.POST['id_habitacion'])
                print(id_reserva)
                reserva=Reserva(
                localizador=id_reserva,
                id_habitacion=Habitaciones.Habitacion.objects.get(id_habitacion=request.POST['id_habitacion']),
                id_cliente=Clientes.Cliente.objects.get(id_cliente=id_cliente),
                huespedes=request.POST['huesped'],
                fx_entrada=fx_entrada,
                fx_salida=fx_salida,
                cuantia_total=cuantia_total)
                reserva.save()
                
                #Se renderiza la vista index en función de la respuesta obtenida.
                self.context['reserva']='Se ha creado su reserva con el siguiente localizador: '+id_reserva
                return render(request,self.template_name,self.context)
            else:
                self.context['reserva']='La habitación que ha selecionado acaba de ser registrada.'
                return render (request,self.template_name,self.context)
        else:
            self.context['reserva']='No se ha podido generar tu reserva vuelva a intentarlo mas tarde.'
            return render (request,self.template_name,self.context)


class MostrarRegistrosClave(View):
    template_name = 'buscarregistro.html'
    def get(self, request,*args, **kwargs): 
        form = BuscarClaveForm()
        context = {'form':form}
        return render(request,self.template_name,context)
    def post(self, request,*args, **kwargs): 
        form = BuscarClaveForm(request.POST)
        print('post',request.POST)
        if form.is_valid():
            clave = str(request.POST['clave'])
            tipo = 0
            if clave.startswith('C'):
                tipo=1
            elif clave.startswith('DOB'):
                tipo=2
            elif clave.startswith('RHA'):
                tipo=3
            else:
                respuesta = 'La clave enviada no es correcta.'
            registro = Reserva.mostrarReservas(tipo,clave)
        print(tipo,registro)
        return render (request,self.template_name)



class MostrarReservas(View):
    template_name = 'index.html'
    def get(self, request,*args, **kwargs): 
        fx_salida=date.today().strftime('%Y-%m-%d')
        registros = Reserva.objects.filter(fx_salida__gte = fx_salida)
        context = {'registros':registros}
        return render(request,self.template_name,context)