from django.shortcuts import render, redirect, get_object_or_404
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
            messages.success(request, "Tarea creada perfectamente")
            return redirect ('lista_tarea')
    else:
        formulario = TareaForms()
    return render (request, 'tarea/crear_tarea.html', {'formulario': formulario})

@login_required
@permission_required('app.delete_tarea')
def eliminar_tarea(request, id_tarea):
    tarea = Tarea.objects.get(id = id_tarea, usuario_id = request.user.id)

    try:
        tarea.delete()
        messages.success(request, "Se ha eliminado la tarea correctamente.")
    except Exception as error:
        print(error)

    return redirect('lista_tarea') 


@login_required
@permission_required('app.change_tarea')
def editar_tarea (request, id_tarea):
    tarea = Tarea.objects.get(id = id_tarea, usuario_id = request.user.id)
    
    if request.method == "POST":
        formulario = TareaForms(request.POST, instance=tarea)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Se ha modificado la tarea correctamente')
            return redirect ('lista_tarea')
        
    else:

        formulario = TareaForms(instance=tarea)     
    return render(request, 'tarea/editar_tarea.html', {'formulario': formulario, 'tarea': tarea})


#Proyecto

@login_required
@permission_required('app.add_proyecto')
def crear_proyecto(request):
    if request.method == 'POST':
        formulario = ProyectoForm(request.POST)
        if formulario.is_valid():
            proyecto = Proyecto.objects.create(
                nombre = formulario.cleaned_data.get('nombre'),
                descripcion = formulario.cleaned_data.get('descripcion'),
                fecha_fin = formulario.cleaned_data.get('fecha_fin'),
                usuario_id = request.user.id
            )
            proyecto.save()
            messages.success(request, "Proyecto creado perfectamente")
            return redirect ('lista_proyecto')
    else:
        formulario = ProyectoForm()
    return render (request, 'proyecto/crear_proyecto.html', {'formulario': formulario})

@login_required
def listar_proyecto(request):
    proyecto = Proyecto.objects.filter(usuario_id = request.user.id)
    return render (request, 'proyecto/listar_proyecto.html', {'proyectos' : proyecto})   




@login_required
@permission_required('app.change_proyecto')
def asignar_proyecto_tarea(request, id_tarea):
    tarea = Tarea.objects.filter(id=id_tarea, usuario=request.user).first()
    if not tarea:
        messages.error(request, "No se encontró la tarea.")
        return redirect('lista_tarea')

    if request.method == 'POST':
        formulario = AsignarProyectoForm(request.POST, instance=tarea, user=request.user)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "La tarea " + tarea.titulo + " se ha asignado correctamente al proyecto")
            return redirect('lista_tarea')
    else:
        formulario = AsignarProyectoForm(instance=tarea, user=request.user)

    return render(request, 'proyecto/asignar_proyecto.html', { 'formulario': formulario, 'tarea': tarea })


@login_required
@permission_required('app.view_proyecto')
def detalle_proyecto(request, id_proyecto):
    proyecto = Proyecto.objects.filter(id=id_proyecto, usuario=request.user).first()
    if not proyecto:
        messages.error(request, "No se encontró el proyecto.")
        return redirect('lista_proyecto')

    tareas = proyecto.tareas.all() 
    return render(request, 'proyecto/detalle_proyecto.html', { 'proyecto': proyecto, 'tareas': tareas })


@login_required
@permission_required('app.change_proyecto')
def editar_proyecto(request, id_proyecto):
    proyecto = Proyecto.objects.filter(id=id_proyecto, usuario=request.user).first()

    if not proyecto:
        messages.error(request, "No se encontró el proyecto o no tienes permisos.")
        return redirect('lista_proyecto')

    if request.method == 'POST':
        formulario = ProyectoForm(request.POST, instance=proyecto)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "El Proyecto " + proyecto.nombre + " se ha modificado correctamente")
            return redirect('lista_proyecto')
    else:
        formulario = ProyectoForm(instance=proyecto)

    return render(request, 'proyecto/editar_proyecto.html', { 'formulario': formulario, 'proyecto': proyecto })  


@login_required
@permission_required('app.delete_proyecto')
def eliminar_proyecto(request, id_proyecto):
    proyecto = Proyecto.objects.filter(id=id_proyecto, usuario=request.user).first()

    if not proyecto:
        messages.error(request, "No se encontró el proyecto o no tienes permisos.")
        return redirect('lista_proyecto')

    if request.method == 'POST':
        proyecto.delete()
        messages.success(request, "El Proyecto " + proyecto.nombre + " se ha eliminado correctamente")
        return redirect('lista_proyecto')

    return render(request, 'proyecto/eliminar_proyecto.html', { 'proyecto': proyecto })
