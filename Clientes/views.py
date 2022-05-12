from django.shortcuts import render
from django.views import View
from .form import crearClienteForm,modificarClienteForm
from .models import Cliente
# Create your views here.

# Clase para crear una nueva habitación a través de un formulario.
class altaCliente(View):
    template_name='alta_cliente.html'
    def get(self, request,*args, **kwargs):
        form=crearClienteForm()
        context={'form':form}
        return render(request,self.template_name,context)
    def post(self, request,*args, **kwargs):
        form=crearClienteForm(request.POST)
        if form.is_valid(): 
            alta , cliente = Cliente.definePkCliente(request.POST.get('nombre'),request.POST.get('apellido'),request.POST.get('email'))
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
    #Con esta clase cualquiera que conozca el campo clave puede modificar el registro, por lo que el campo clave se deberia recoger durante 
    #un proceso de login previo y ser enviado desde la sesión o cookie al logearse.
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
            Cliente.updateCliente(request.POST.get('id_cliente'),request.POST.get('nombre'),request.POST.get('apellido'),request.POST.get('email'))
            respuesta = 'Datos modificados con éxito.'
        else:
            respuesta = 'No se podido modificar ningún registro vuelva a intentarlo mas tarde.'
        args=respuesta
        return self.get(request, args)
 ## de clientes se necesita solo el read de los datos de este y el delete 