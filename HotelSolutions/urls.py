"""HotelSolutions URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from cgitb import handler
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from Habitaciones import views as habitacion
from Reservas import views as reserva
from Clientes import views as cliente


urlpatterns = [

  
    #URLs-Habitaciones
    path('mostrarhabitaciones/', habitacion.listarHabitaciones , name='listarHabitaciones'),
    path('crearHabitacion', habitacion.crearHabitación.as_view() ,name='crearHabitacion'),
    path('udHabitacion/<str:servicio>', habitacion.udHabitación.as_view() ,name='udHabitacion'),

    #URLs-cliente
    path('altacliente/', cliente.altaCliente.as_view() , name='altacliente'),
    path('modificarcliente/', cliente.modificarCliente.as_view() , name='modificarcliente'),


    #URLs-Reservas
    path('',reserva.MostrarReservas.as_view(),name='inicio'),
    path('confirmar_reserva',reserva.ConfirmarReserva.as_view(),name='confirmar_reserva'),
    path('buscar_reserva/',reserva.MostrarRegistrosClave.as_view() ,name='buscar_reserva'),
    path('contratacion/',reserva.comprobarDisponibilidad.as_view(),name='contratacion'),
    


    #admin 
    path('admin/', admin.site.urls),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'Reservas.views.view_404'
