from tabnanny import verbose
from django import forms 

class DisponibilidadForm(forms.Form):
    fx_inicio = forms.DateField(label='entrada')
    fx_salida = forms.DateField(label='salida')
    huespedes = forms.IntegerField(max_value=10, label='huespedes')
