import json
from datetime import datetime,timedelta,date
from django.db.models import Q
from django.shortcuts import  render, redirect
from django.views import View
from Clientes.form import crearClienteForm
from .forms import DisponibilidadForm,BuscarClaveForm
from .models import Habitaciones,Reserva,Precio, Clientes



# Create your views here.

#Clase con las vistas para generar el formulario que recoge la fecha entrada, fecha salida y los huéspedes que se alojan.
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
            context={'error':'No se puedes seleccionar una fecha maxima por encima de 2022-12-31','form':self.form}
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
        #la fecha de salida de la habitación no coincide con la nueva entrada
        #la entrada del nuevo huésped coincide con la entrada o próximas entradas de huéspedes --fx_entrada__gte = fx_entrada-- 
        #la salida del huéspedes no coincide con la entrada de otros huéspedes --fx_entrada__lte=fx_salida--
        #Con esto obtenemos todas las habitaciones ocupadas en el rango de fechas proporcionado en la petición. 
        disp = Reserva.objects.filter(Q(fx_salida__gte=fx_entrada) | Q(fx_entrada__gte = fx_entrada) & Q(fx_entrada__lte=fx_salida))
        print (disp)
        reg = []
        for hab in disp:
            if hab != None: 
                reg.append(getattr( getattr(hab,'id_habitacion'),'id_habitacion'))
        # Esta no es la manera mas optima de obtener todos los registros ya que con consulta INNERJOIN se pueda realizar en un único acceso a BBDD
        # pero con mis conocimientos actuales es la única manera que conozco
        #Discriminador para mostrar las habitaciones que puedan albergar todos los huéspedes.
        habitaciones_disponibles = Habitaciones.Habitacion.objects.filter(tipo_habitacion__gte = request.POST.get('huespedes')).exclude(id_habitacion__in=reg)
        #Calculo de la tabla de disponibilidad
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
        #{url: imagen asociada, habitacion: id_habitacion, huespedes: num_personas_max, precio: cuantia_total_estancia con moneda}
        # devolvemos esta tabla generada
        tabla_final = []
        for habitacion in habitaciones_disponibles: 
            tupla={}
            tupla['url']='../'+str(getattr(habitacion,'imagen'))
            tupla['habitacion']=getattr(habitacion,'id_habitacion')
            tupla['huespedes']=getattr(habitacion,'tipo_habitacion')
            tupla['precio']= str(float(precios[str(getattr(habitacion,'tipo_habitacion'))]) * num_dias) + moneda
            tabla_final.append(tupla)
        data = json.dumps(tabla_final)      
        return data

#Vista para realizar la reserva con los datos enviados por el cliente
#Solo se podrá llegar a esta vista con una petición POST
class ConfirmarReserva(View):
    template_name='index.html'
    registros = Reserva.objects.filter(fx_salida__gte = date.today().strftime('%Y-%m-%d'))
    context={}
    context['registros']=registros

    def post(self, request,*args, **kwargs):
        id_cliente = Clientes.Cliente.comprobarCliente(request.POST['nombre'],request.POST['apellido'],request.POST['email'],request.POST['tlf'])
        if id_cliente != 1:
            #Una vez recibido el ID del cliente se realiza la verificación de la habitación no este reservada.
            fx_salida = request.POST['fx_salida']
            fx_entrada = request.POST['fx_entrada']

            #Antes de realizar el alta comprobamos que la habitación no haya sido ocupada en el transcurso.
            if not Reserva.objects.filter(id_habitacion = request.POST['id_habitacion'],fx_entrada__gte = fx_entrada ,fx_entrada__lte=fx_salida):
                #Volvemos a calcular el importe servidor para evitar la posible modificación de precios por clientes.
                dias = (datetime.strptime(fx_salida,'%Y-%m-%d') - datetime.strptime(fx_entrada,'%Y-%m-%d'))/timedelta(days=1)
                cuantia_total = Precio.calcularPrecio(dias,request.POST['id_habitacion'])

                #Se almacena la reserva.
                id_reserva = Reserva.defineLocalizador(request.POST['id_habitacion'])
                reserva=Reserva(
                localizador=id_reserva,
                id_habitacion=Habitaciones.Habitacion.objects.get(id_habitacion=request.POST['id_habitacion']),
                id_cliente=Clientes.Cliente.objects.get(id_cliente=id_cliente),
                huespedes=request.POST['huesped'],
                fx_entrada=fx_entrada,
                fx_salida=fx_salida,
                cuantia_total=cuantia_total)
                reserva.save()
                
        #Se genera la vista index en función de la respuesta obtenida.
        #Esta vista se renderiza a través de Jquery
                self.context['reserva']='Se ha creado su reserva con el siguiente localizador: '+id_reserva
                return render(request,self.template_name,self.context)
            else:
                self.context['reserva']='La habitación que ha selecionado acaba de ser registrada.'
                return render (request,self.template_name,self.context)
        else:
            self.context['reserva']='No se ha podido generar tu reserva vuelva a intentarlo mas tarde.'
            return render (request,self.template_name,self.context)

#Vista para mostrar las reservas asociadas a la clave de:
# 1 = Clave de Cliente
# 2 = Clave de Habitación
# 3 = Localizador de Reserva
class MostrarRegistrosClave(View):
    template_name = 'buscarregistro.html'
    form = BuscarClaveForm()
    context = {}
    def get(self, request,*args, **kwargs): 
        self.context = {'form':self.form}
        return render(request,self.template_name,self.context)
    def post(self, request,*args, **kwargs): 
        self.context['registros']=''
        form = BuscarClaveForm(request.POST)
        if form.is_valid():
            clave = str(request.POST['clave'])
            tipo = 0
            if clave.startswith('C'):
                tipo=1
            elif clave.startswith('HA'):
                tipo=2
            elif clave.startswith('RHA'):
                tipo=3
            else:
                self.context['form'] = self.form
                self.context['respuesta'] = 'La clave enviada no es correcta.'
            if tipo != 0:    
                registro = Reserva.mostrarReservas(tipo,clave)
                self.context['registros'] = registro
        else:
            self.context['form'] = self.form
            self.context['respuesta'] = 'No se ha podido verificar una respuesta, vuelva a intentarlo mas tarde.'
        return render (request,self.template_name,self.context)



class MostrarReservas(View):
#Se genera la pagina de inicio con el registro de todas las reservas activas que tenga fecha de salida superior o igual a la fecha actual
    template_name = 'index.html'
    def get(self, request,*args, **kwargs): 
        registros = Reserva.objects.filter(fx_salida__gte = date.today().strftime('%Y-%m-%d'))
        context = {'registros':registros}
        return render(request,self.template_name,context)

def view_404(request,exception=None):
    return redirect('inicio')