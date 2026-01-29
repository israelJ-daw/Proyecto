from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.index, name='index'),

    path('registro/', views.registrar_usuario, name='registro'), 

    path('lista_tarea/', views.listar_tarea, name= 'lista_tarea'),
    path('crear_tarea/', views.crear_tarea, name='crear_tarea'),
    path('eliminar/tarea/<int:id_tarea>', views.eliminar_tarea, name='eliminar_tarea'),
    path('editar/tarea/<int:id_tarea>', views.editar_tarea, name='editar_tarea'),

    #Proyecto
    path('lista_proyecto/', views.listar_proyecto, name= 'lista_proyecto'),
    path('crear_proyecto/', views.crear_proyecto, name='crear_proyecto'),
    path('detalle_proyecto/<int:id_proyecto>/', views.detalle_proyecto, name='detalle_proyecto'),
    path('asignar_proyecto/<int:id_tarea>/', views.asignar_proyecto_tarea, name='asignar_proyecto_tarea'),
    path('editar_proyecto/<int:id_proyecto>/', views.editar_proyecto, name='editar_proyecto'),
    path('eliminar_proyecto/<int:id_proyecto>/', views.eliminar_proyecto, name='eliminar_proyecto'),

]