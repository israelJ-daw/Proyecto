from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroForm
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


def index(request):
    return render(request, 'index.html', {})


def registrar_usuario(request):
    if request.method == 'POST':
        formulario = RegistroForm(request.POST)
        if formulario.is_valid():
            user = formulario.save()

            grupo = Group.objects.get(name='Usuario')
            user.groups.add(grupo)

            login(request, user)      
            return redirect('index')   
    else:
        formulario = RegistroForm()  

    return render(request, 'registration/signup.html', {'formulario': formulario})
 

@login_required
@permission_required('app.view_tarea')
def listar_tarea(request):
  tarea = Tarea.objects.filter(usuario_id = request.user.id)
  return render (request, 'tarea/lista_tarea.html', {'tareas' : tarea})

@login_required
@permission_required('app.add_tarea')
def crear_tarea(request):
    if request.method == 'POST':
        formulario = TareaForms(request.POST)
        if formulario.is_valid():
            tarea = Tarea.objects.create(

                titulo = formulario.cleaned_data.get('titulo'),
                descripcion = formulario.cleaned_data.get('descripcion'),
                estado = formulario.cleaned_data.get('estado'),
                prioridad = formulario.cleaned_data.get('prioridad'),
                fecha_vencimiento = formulario.cleaned_data.get('fecha_vencimiento'),
                usuario_id = request.user.id
            )
            tarea.save()
            messages.success ("Tarea creada Perfectamente")
            return redirect ('lista_tarea')
    else:
        formulario = TareaForms()
    return render (request, 'tarea/crear_tarea.html', {'formulario': formulario})

@login_required
@permission_required('app.delete_tarea')
def eliminar_tarea(request, id_tarea):
    tarea = Tarea.objects.get(id = id_tarea)

    try:
        tarea.delete()
        messages.success(request, "Se ha eliminado la tarea correctamente.")
    except Exception as error:
        print(error)

    return redirect('lista_tarea') 


@login_required
@permission_required('app.change_tarea')
def editar_tarea (request, id_tarea):
    tarea = Tarea.objects.get(id = id_tarea)
    
    if request.method == "POST":
        formulario = TareaForms(request.POST, instance=tarea)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Se ha modificado la tarea correctamente')
            return redirect ('lista_tarea')
        
    else:

        formulario = TareaForms(instance=tarea)
    return render(request, 'tarea/editar_tarea.html', {'formulario': formulario, 'tarea': tarea})
