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
        


class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'fecha_fin']
        widgets = {
            'fecha_fin': forms.DateInput(attrs={'type': 'date'})
        }

class AsignarProyectoForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['proyecto']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Mostrar solo proyectos del usuario actual
            self.fields['proyecto'].queryset = Proyecto.objects.filter(usuario=user)
            self.fields['proyecto'].empty_label = "Selecciona un proyecto"

class SubtareaForm(forms.ModelForm):
    class Meta:
        model = Subtarea
        fields = ['titulo', 'descripcion', 'fecha_vencimiento', 'completada']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
            'fecha_vencimiento': forms.DateInput(attrs={'type':'date', 'class': 'form-control'}),
            'completada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CategoriaForm(forms.ModelForm):

    class Meta:
        model = Categoria
        fields = ["nombre", "descripcion"]

        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej: Frontend, Trabajo, Universidad..."
            }),

            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Añade una breve descripción de la categoría (opcional)..."
            }),
        }