from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from urllib3 import request
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

            grupo, creado = Group.objects.get_or_create(name='Usuario')
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
  buscar = request.GET.get("buscar")
  estado = request.GET.get("estado")
  prioridad = request.GET.get("prioridad")
  proyecto = request.GET.get("proyecto")
  proyectos = Proyecto.objects.filter(usuario=request.user)
  categoria = request.GET.get("categoria")
  categorias = Categoria.objects.filter(usuario=request.user)
  orden = request.GET.get("orden")
  
  if buscar:
        tarea = tarea.filter(titulo__icontains = buscar)
  if estado:
        tarea = tarea.filter(estado = estado)
  if prioridad:
      tarea = tarea.filter(prioridad = prioridad)
  if proyecto:
      tarea = tarea.filter(proyecto_id=proyecto)
  if categoria:
        tarea = tarea.filter(categoria_id=categoria)
  if orden:
      if orden == "recientes":
            tarea = tarea.order_by('fecha_creacion')
      elif orden == "antiguas":
            tarea = tarea.order_by('-fecha_creacion')
      elif orden == "vencimiento":
            tarea = tarea.order_by('fecha_vencimiento')
      elif orden == "prioridad_alta":
            tarea = tarea.order_by('prioridad')
      elif orden == "prioridad_baja":
            tarea = tarea.order_by('-prioridad')
      elif orden == "az":
            tarea = tarea.order_by('titulo')
      elif orden == "za":
            tarea = tarea.order_by('-titulo')
  else:
      tarea = tarea.order_by('-fecha_creacion')
  return render (request, 'tarea/lista_tarea.html', {'tareas' : tarea, 'proyectos': proyectos , 'categorias': categorias})


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
    buscar = request.GET.get("buscar")
    if buscar:
        proyecto = proyecto.filter(nombre__icontains = buscar)

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

    proyecto = Proyecto.objects.filter(id=id_proyecto,usuario=request.user).first()

    if not proyecto:
        messages.error(request, "No se encontró el proyecto.")
        return redirect('lista_proyecto')

    tareas = proyecto.tareas.all()

    buscar = request.GET.get("buscar")
    estado = request.GET.get("estado")
    prioridad = request.GET.get("prioridad")

    if buscar:
        tareas = tareas.filter(titulo__icontains=buscar)

    if estado:
        tareas = tareas.filter(estado=estado)

    if prioridad:
        tareas = tareas.filter(prioridad=prioridad)

    return render(
        request,
        'proyecto/detalle_proyecto.html', {'proyecto': proyecto,'tareas': tareas,})


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

#SubTareas

@login_required
@permission_required('app.view_subtarea')
def listar_subtareas(request, id_tarea):
 
    subtareas = Subtarea.objects.filter(tarea__id=id_tarea, tarea__usuario=request.user)
    
    tarea = Tarea.objects.filter(id=id_tarea, usuario=request.user).first()

    buscar = request.GET.get("buscar")
    if buscar:
        subtareas = subtareas.filter(titulo__icontains=buscar)
    if not tarea:
        messages.error(request, "No se encontró la tarea.")
        return redirect('lista_tarea')
    
    return render(request, 'subtarea/listar_subtareas.html', {'tarea': tarea, 'subtareas': subtareas })    


@login_required
@permission_required('app.add_subtarea')
def crear_subtarea(request, id_tarea):
    tarea = Tarea.objects.filter(id=id_tarea, usuario=request.user).first()
    if not tarea:
        messages.error(request, "No se encontró la tarea.")
        return redirect('lista_tarea')
    
    if request.method == 'POST':
        formulario = SubtareaForm(request.POST)
        if formulario.is_valid():
            Subtarea.objects.create(
                titulo=formulario.cleaned_data.get("titulo"),
                descripcion=formulario.cleaned_data.get("descripcion"),
                fecha_vencimiento=formulario.cleaned_data.get("fecha_vencimiento"),
                completada=formulario.cleaned_data.get("completada"),
                tarea=tarea
            )
            messages.success(request, "Subtarea creada correctamente")
            # Redirige a la lista de subtareas de esta tarea
            return redirect('listar_subtareas', id_tarea=tarea.id)
    else:
        formulario = SubtareaForm()
    
    # Renderiza un template solo con el formulario
    return render(request, 'subtarea/crear_subtarea.html', {'formulario': formulario, 'tarea': tarea})


@login_required
@permission_required('app.change_subtarea')
def editar_subtarea(request, id_subtarea):
    subtarea = Subtarea.objects.filter(id=id_subtarea, tarea__usuario=request.user).first()
    if not subtarea:
        messages.error(request, "No se encontró la subtarea.")
        return redirect('lista_tarea')
    
    if request.method == 'POST':
        formulario = SubtareaForm(request.POST, instance=subtarea)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Subtarea modificada correctamente")
            return redirect('listar_subtareas', id_tarea=subtarea.tarea.id)
    else:
        formulario = SubtareaForm(instance=subtarea)
    
    return render(request, 'subtarea/editar_subtarea.html', { 'formulario': formulario, 'subtarea': subtarea})

@login_required
@permission_required('app.delete_subtarea')
def eliminar_subtarea(request, id_subtarea):
    subtarea = Subtarea.objects.filter(id=id_subtarea, tarea__usuario=request.user).first()
    if not subtarea:
        messages.error(request, "No se encontró la subtarea.")
        return redirect('lista_tarea')
    
    if request.method == 'POST':
        subtarea.delete()
        messages.success(request, "Subtarea eliminada correctamente")
        return redirect('listar_subtareas', id_tarea=subtarea.tarea.id)
    
    return render(request, 'subtarea/eliminar_subtarea.html', {'subtarea': subtarea})

#Categoria

@login_required
@permission_required('app.view_categoria')
def listar_categoria(request):
    categorias = Categoria.objects.filter(usuario=request.user)
    buscar = request.GET.get("buscar")
    if buscar:
        categorias = categorias.filter(nombre__icontains=buscar)


    return render(request,'categoria/lista_categoria.html', {'categorias': categorias})

@login_required
@permission_required('app.add_categoria')
def crear_categoria(request):

    if request.method == "POST":
        formulario = CategoriaForm(request.POST)

        if formulario.is_valid():
            Categoria.objects.create(
                nombre=formulario.cleaned_data.get("nombre"),
                descripcion=formulario.cleaned_data.get("descripcion"),
                usuario=request.user
            )

            messages.success(request, "Categoría creada correctamente.")
            return redirect("lista_categoria")

    else:
        formulario = CategoriaForm()

    return render(
        request, "categoria/crear_categoria.html", {'formulario': formulario})

@login_required
@permission_required('app.change_categoria')
def editar_categoria(request, id_categoria):

    categoria = Categoria.objects.filter(id = id_categoria, usuario=request.user).first()
    if not categoria:
        messages.success (request, "No se encontro la categoria")
        return redirect ('lista_categoria')
    
    if request.method == 'POST':
        formulario = CategoriaForm(request.POST, instance=categoria)
        if formulario.is_valid():
            formulario.save()
            messages.error (request, "Categoria actualizada correctemente")
            return redirect ('lista_categoria')
    else:
        formulario = CategoriaForm(instance=categoria)

    return render (request, 'categoria/editar_categoria.html', {'formulario' : formulario, 'categoria' : categoria})


@login_required
@permission_required('app.delete_categoria')
def eliminar_categoria(request, id_categoria):
    categoria  = Categoria.objects.filter(id = id_categoria, usuario=request.user).first()
    if not categoria:
        messages.error(request, "Categoria no encontrada")
        return redirect ('lista_categoria')
    
    if request.method == 'POST':
        categoria.delete()
        messages.success(request , "Categoria elimanda correctamente")
        return redirect ('lista_categoria')

    return render (request, 'categoria/eliminar_categoria.html', {'categoria' : categoria})

@login_required
@permission_required('app.change_categoria')
def asignar_categoria_tarea(request, id_tarea):

    tarea = Tarea.objects.filter( id=id_tarea,usuario=request.user).first()

    if not tarea:
        messages.error(request, "No se encontró la tarea.")
        return redirect("lista_tarea")

    categorias = Categoria.objects.filter(usuario=request.user)

    if request.method == "POST":

        categoria_id = request.POST.get("categoria")

        categoria = Categoria.objects.filter(id=categoria_id,usuario=request.user).first()

        if categoria:
            tarea.categoria = categoria
            tarea.save()

            messages.success(request, "Categoría asignada correctamente.")
            return redirect("lista_tarea")
        else:
            messages.error(request, "La categoría seleccionada no es válida.")

    return render(request,"categoria/asignar_categoria_tarea.html",{"tarea": tarea,"categorias": categorias})


from django.http import JsonResponse
from django.db.models import Q

@login_required
@permission_required('app.view_tarea')
def buscar_tarea(request):

    buscar = request.GET.get("buscar", "")

    tareas = Tarea.objects.filter(usuario = request.user).filter(Q(titulo__icontains=buscar))

    resultados = []

    for tarea in tareas:

        resultados.append({
            "id": tarea.id,
            "titulo": tarea.titulo,
            "descripcion": tarea.descripcion,
            "estado": tarea.estado,
            "prioridad": tarea.prioridad,
            "fecha_vencimiento": tarea.fecha_vencimiento.strftime("%d/%m/%Y") if tarea.fecha_vencimiento else None,
            "completada": tarea.completada,

            "proyecto": {
                "id": tarea.proyecto.id,
                "nombre": tarea.proyecto.nombre,
            } if tarea.proyecto else None,

            "categoria": {
                "id": tarea.categoria.id,
                "nombre": tarea.categoria.nombre,
                "descripcion": tarea.categoria.descripcion,
            } if tarea.categoria else None,
        })

    return JsonResponse(resultados, safe=False)


@login_required
@permission_required('app.view_subtarea')
def buscar_subtarea(request, id_tarea):

    buscar = request.GET.get("buscar", "")

    tarea = Tarea.objects.filter(
        id=id_tarea,
        usuario=request.user).first()

    subtareas = Subtarea.objects.filter(
        tarea=tarea,
        titulo__icontains=buscar)

    resultados = []

    for subtarea in subtareas:

        resultados.append({
            "id": subtarea.id,
            "titulo": subtarea.titulo,
            "descripcion": subtarea.descripcion,
            "completada": subtarea.completada,
            "fecha_vencimiento": subtarea.fecha_vencimiento,
        })

    return JsonResponse(resultados, safe=False)

@login_required
def buscar_proyecto(request):

    buscar = request.GET.get("buscar")

    proyectos = Proyecto.objects.filter(
        usuario=request.user
    ).filter(
        Q(nombre__icontains=buscar)
    )

    datos = []

    for proyecto in proyectos:

        datos.append({
            "id": proyecto.id,
            "nombre": proyecto.nombre,
            "descripcion": proyecto.descripcion,
            "fecha_creacion": proyecto.fecha_creacion.strftime("%d/%m/%Y"),
            "fecha_fin": proyecto.fecha_fin.strftime("%d/%m/%Y") if proyecto.fecha_fin else None
        })

    return JsonResponse(datos, safe=False)