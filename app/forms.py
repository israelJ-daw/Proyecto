from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class RegistroForm(UserCreationForm):  
    ROLES = (
        (Usuario.USUARIO, 'usuario'),

    )
    
    rol = forms.ChoiceField(choices=ROLES)

    class Meta:
        model = Usuario  
        fields = ('username', 'email', 'password1', 'password2', 'rol')  


class TareaForms(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'estado', 'prioridad', 'fecha_vencimiento']
        widgets = {
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
        }
        