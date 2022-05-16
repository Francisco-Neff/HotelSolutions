
import datetime
from django import forms

DATE_INPUT_FORMATS = ('%d/%m/%Y')


class DisponibilidadForm(forms.Form):
    #Formulario para comprobar la disponibilidad, se añade al campo fecha de entrada la fecha actual.
    fx_entrada = forms.DateField(label='Fecha de entrada',initial=datetime.datetime.today().strftime('%d/%m/%Y') ,input_formats=DATE_INPUT_FORMATS)
    fx_salida = forms.DateField(label='Fecha de salida')
    huespedes = forms.IntegerField(max_value=4, label='Huespedes')
    #Nota: Se pone 4 personas como máximo ya que es el tope de una habitación, pero se deberia implementar un método que pregunte al usuario si son
    # mas de 4 como se quiere alojar 
    # Ejemplo, una reserva para 6 personas:
        # Todos individuales
        # 3 dobles
        # 2 triples
        # Otra (Definida por el usuario)


   
