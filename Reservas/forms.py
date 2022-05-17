import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django import forms

DATE_INPUT_FORMATS = ('%d/%m/%Y')


class DisponibilidadForm(forms.Form):
    #Formulario para comprobar la disponibilidad, se añade al campo fecha de entrada la fecha actual.
    fx_entrada = forms.DateField(label='Fecha de entrada',initial=datetime.datetime.today().strftime('%d/%m/%Y') ,input_formats=DATE_INPUT_FORMATS,validators=[MaxValueValidator('31/12/2022'),MinValueValidator(datetime.datetime.today().strftime('%d/%m/%Y'))])
    fx_salida = forms.DateField(label='Fecha de salida',input_formats=DATE_INPUT_FORMATS,validators=[MaxValueValidator('31/12/2022'),MinValueValidator(datetime.datetime.today().strftime('%d/%m/%Y'))])
    huespedes = forms.IntegerField(max_value=4, label='Huespedes')
    #Nota: Se pone 4 personas como máximo ya que es el tope de una habitación, pero se deberia implementar un método que pregunte al usuario si son
    # mas de 4 como se quiere alojar 
    # Ejemplo, una reserva para 6 personas:
        # Todos individuales
        # 3 dobles
        # 2 triples
        # Otra (Definida por el usuario)

class BuscarClaveForm(forms.Form):
    #Formulario para mostrar todas las reservas por una clave de cliente, habitación o localizador
    clave = forms.CharField(max_length=10, label='Introduce la clave de busqueda')
   
