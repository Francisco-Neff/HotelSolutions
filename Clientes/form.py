from django import forms
from .models import Cliente

class crearClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields=['nombre','apellido','email']
    
class modificarClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields=['id_cliente','nombre','apellido','email']



