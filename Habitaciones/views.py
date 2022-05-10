from django.shortcuts import render
from.models import Habitacion

# Create your views here.

def homepage(request):
    return render(request,'index.html')



def listarHabitaciones(request):
    print('lista habitaciones')
    list_habitaciones = Habitacion.objects.all()
    print(list_habitaciones)
    context={'registros':list_habitaciones}
    return render(request,'listar_habitaciones.html',context)

