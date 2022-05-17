from django import forms
from .models import Habitacion

class crearHabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields=['tipo_habitacion','n_habitacion','imagen']

class borrarHabitacionForm(forms.Form):
    id_borrar = forms.IntegerField(max_value=6, label='Introduzca la clave')
