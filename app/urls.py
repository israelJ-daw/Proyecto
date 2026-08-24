from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.index, name='index'),

    path('registro/', views.registrar_usuario, name='registro'), 

    path('lista_tarea/', views.listar_tarea, name= 'lista_tarea'),
    path('crear_tarea/', views.crear_tarea, name='crear_tarea'),
    path('eliminar/tarea/<int:id_tarea>', views.eliminar_tarea, name='eliminar_tarea'),
    path('editar/tarea/<int:id_tarea>', views.editar_tarea, name='editar_tarea'),
    path('buscar_tarea/', views.buscar_tarea, name='buscar_tarea'),

    #Proyecto
    path('lista_proyecto/', views.listar_proyecto, name= 'lista_proyecto'),
    path('crear_proyecto/', views.crear_proyecto, name='crear_proyecto'),
    path('detalle_proyecto/<int:id_proyecto>/', views.detalle_proyecto, name='detalle_proyecto'),
    path('asignar_proyecto/<int:id_tarea>/', views.asignar_proyecto_tarea, name='asignar_proyecto_tarea'),
    path('editar_proyecto/<int:id_proyecto>/', views.editar_proyecto, name='editar_proyecto'),
    path('eliminar_proyecto/<int:id_proyecto>/', views.eliminar_proyecto, name='eliminar_proyecto'),

    #SubTareas
    path('listar_subtareas/<int:id_tarea>/', views.listar_subtareas, name='listar_subtareas'),
    path('crear_subtarea/<int:id_tarea>/', views.crear_subtarea, name='crear_subtarea'),
    path('editar_subtarea/<int:id_subtarea>/', views.editar_subtarea, name='editar_subtarea'),
    path('eliminar_subtarea/<int:id_subtarea>/', views.eliminar_subtarea, name='eliminar_subtarea'),

    #Categoria
    path('listar_categoria/', views.listar_categoria, name='lista_categoria'),
    path('crear_categoria/', views.crear_categoria, name='crear_categoria'),
    path('editar_tarea/<int:id_categoria>/', views.editar_categoria, name = 'editar_categoria'),
    path('eliminar_categoria/<int:id_categoria>/' , views.eliminar_categoria, name='eliminar_categoria'),
    path('asignar_categoria_tarea/<int:id_tarea>/', views.asignar_categoria_tarea, name='asignar_categoria_tarea'),


    path('buscar_subtarea/<int:id_tarea>/', views.buscar_subtarea, name='buscar_subtarea'),
]