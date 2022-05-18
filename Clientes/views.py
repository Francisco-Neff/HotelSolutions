from django.shortcuts import render
from django.views import View
from .form import crearClienteForm,modificarClienteForm
from .models import Cliente
# Create your views here.

##Todas estas vistas estarían pensadas para utilizarse con un proceso de login como verificación,
##ademas de usar sesiones para tener los datos de cliente almacenados y ahorrar al cliente que tenga que rellenar sus datos 
##en el proceso de de una nueva reserva. 

## Para clientes solo se crean los métodos de crear y modificar.

# Clase para crear un nuevo cliente a través de un formulario.
class altaCliente(View):
    template_name='alta_cliente.html'
    def get(self, request,*args, **kwargs):
        form=crearClienteForm()
        context={'form':form}
        return render(request,self.template_name,context)
    def post(self, request,*args, **kwargs):
        form=crearClienteForm(request.POST)
        if form.is_valid(): 
            alta , cliente = Cliente.definePkCliente(request.POST.get('nombre'),request.POST.get('apellido'),request.POST.get('email'),request.POST.get('telefono'))
            if alta == 1 :
                respuesta = 'Ha ocurrido un error a crear tu usuario, vuelve a intentarlo en otro momento.'
            else:
                cliente.save()
                respuesta = 'Has sido creado correctamente con tu clave :' + alta
            context={'respuesta': respuesta}
        else:
            form=crearClienteForm()
            context={'form':form}
        return render(request, self.template_name ,context)

class modificarCliente(View):
    #Con esta clase cualquiera que conozca el campo clave puede modificar el registro
    template_name='alta_cliente.html'

    def get(self, request,*args, **kwargs):
        form=modificarClienteForm()
        context={'form':form}
        print(len(args))
        if len(args) > 0:
            context['respuesta'] = args[0] 

        return render(request,self.template_name,context)
    def post(self, request,*args, **kwargs):
        form=modificarClienteForm(request.POST)
        if (request.POST.get('id_cliente') in Cliente.objects.values_list('id_cliente', flat=True)): 
            Cliente.updateCliente(request.POST.get('id_cliente'),request.POST.get('nombre'),request.POST.get('apellido'),request.POST.get('email'),request.POST.get('telefono'))
            respuesta = 'Datos modificados con éxito.'
        else:
            respuesta = 'No se podido modificar ningún registro vuelva a intentarlo mas tarde.'
        args=respuesta
        return self.get(request, args)
