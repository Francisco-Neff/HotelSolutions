from django.shortcuts import render
from django.views import View
from .forms import DisponibilidadForm
# Create your views here.
class comprobarDisponibilidad(View):
    template_name='disponibilidad_form.html'
    def get(self, request,*args, **kwargs):
        form = DisponibilidadForm()
        context={'form':form}
        return render(request,self.template_name,context)
    def post(self, request,*args, **kwargs):
        context={'form':'formulario correcto'}
        return render(request,self.template_name,context)
