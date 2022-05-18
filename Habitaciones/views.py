from calendar import c
from distutils.command.clean import clean
from random import choices
from django.shortcuts import render
from django.views import View
from .models import Habitacion
from .forms import crearHabitacionForm

# Create your views here.

##Todas estas vistas estarían pensadas para utilizarse con un proceso de administrador que pudiera realizar los pasos de alta,modificación, y borrado a este 
## y se dejaría el método de mostrar habitaciones libre para cualquier usuario.

# Se crean las vistas de habitaciones con el concepto CRUD

# Clase para crear una nueva habitación a través de un formulario.
class crearHabitación(View):
    template_name='crear_habitacion.html'
    def get(self, request,*args, **kwargs):
        form=crearHabitacionForm()
        context={'form':form}
        return render(request,self.template_name,context)
    def post(self, request,*args, **kwargs):
        form=crearHabitacionForm(request.POST,request.FILES)
        if form.is_valid(): 
            alta = Habitacion.DefinePkHab.definePkHab(request.POST.get('tipo_habitacion'),request.POST.get('n_habitacion'))
            if alta == 1 :
                respuesta = 'No se puede crear una habitación con estas características'
            else:
                Habitacion.objects.create(
                    id_habitacion=alta,
                    tipo_habitacion=form.cleaned_data.get('tipo_habitacion'),
                    n_habitacion=form.cleaned_data.get('n_habitacion'),
                    imagen=form.cleaned_data.get('imagen')
                )
                respuesta = 'Se ha creado una nueva habitación con la siguiente clave :' + alta
            context={'respuesta': respuesta}
        else:
            respuesta = 'No se puede crear una habitación con estas características'
            form=crearHabitacionForm()
            context={'form':form,'param_error':respuesta}
        return render(request, self.template_name ,context)

# Vista para mostrar todos los datos de las habitaciones actuales
def listarHabitaciones(request):
    list_habitaciones = Habitacion.objects.all() 
    context={'registros':list_habitaciones}
    return render(request,'listar_habitaciones.html',context)

# Clase para eliminar o modificar una habitación a través de la selección de su campo identificador y el parámetro
# servicio enviado mediante la URL.
class udHabitación(View):
    template_name='ud_habitacion.html'

    def get(self, request,servicio,*args, **kwargs):
        query_list = Habitacion.objects.all()
        context={'listado':query_list,'servicio':servicio}       
        if len(args) > 0:
            context['respuesta'] = args[0] 
        return render(request, self.template_name ,context)

    def post(self, request,servicio,*args, **kwargs):
        # si el servicio enviado es borrar, se enviara la clave para su borrado
        # si el servicio enviado es modificar, se enviara la clave al método de modificar para cambiar los datos de la habitación
        # una vez recogidos los datos de este formulario se cambia el servicio a update, para crear un nuevo registro con los datos de esta habitación
        # se crea una nueva para no perder la información de la clave primaria y se procede a eliminar el registro anterior.
        if (request.POST.get('ud') in Habitacion.objects.values_list('id_habitacion', flat=True)) and (request.POST.get('ud') != None): 
            if servicio == 'borrar': 
                args = 'La habitación ha sido borrada con éxito.'
                Habitacion.objects.filter(id_habitacion=request.POST.get('ud')).delete()
                return self.get(request, servicio, args)
            elif servicio == 'modificar':
                args=request.POST.get('ud') #Se envia el identificador habitación
                return self.modificar(request,servicio,args)
            elif servicio == 'update':     
                form=crearHabitacionForm(request.POST,request.FILES)
                if form.is_valid():
                    upt = Habitacion.UpdateHabitacion.updateHabitacion(request.POST.get('ud'),request.POST.get('tipo_habitacion'),request.POST.get('n_habitacion'))
                    if upt == 1:
                        args='Se ha producido un error durante la actualización y esta no se ha realizado'
                    else:
                        Habitacion.objects.create(
                        id_habitacion=upt,
                        tipo_habitacion=form.cleaned_data.get('tipo_habitacion'),
                        n_habitacion=form.cleaned_data.get('n_habitacion'),
                        imagen=form.cleaned_data.get('imagen')
                        )
                        args='Se ha modificación actual creando la nueva clave para esta: '+ upt
                else:
                    args='Se ha producido un error durante la actualización y esta no se ha realizado'
                servicio='modificar'  
                return self.get(request,servicio,args)
        else:
            args='Debes seleccionar alguna opción para continuar'
            return self.get(request,servicio,args)  
    
    #Si se va a modificar una habitación se genera esta vista con el formulario para modificarla.
    def modificar(self, request,servicio,*args, **kwargs):
        if servicio != 'modificar':
            servicio='modificar'
            args='No se ha encontrado la acción que desea realizar'
            return self.get(request,servicio,args)
        else:
            form=crearHabitacionForm()
            context={'form':form,'servicio':'update','ud_id':args[0]}
            return render(request,self.template_name,context)




      



    
        
        
        
