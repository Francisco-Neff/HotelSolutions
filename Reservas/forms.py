
import datetime
from django import forms

DATE_INPUT_FORMATS = ('%d/%m/%Y','%d-%m-%Y')


class DisponibilidadForm(forms.Form):
    fx_entrada = forms.DateField(label='Fecha de entrada',initial=datetime.datetime.today().strftime('%d/%m/%Y') ,input_formats=DATE_INPUT_FORMATS)
    fx_salida = forms.DateField(label='Fecha de salida')
    huespedes = forms.IntegerField(max_value=10, label='huespedes')
    
   
