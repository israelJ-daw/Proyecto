from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.index, name='index'),

    path('registro/', views.registrar_usuario, name='registro'), 

    path('lista_tarea/', views.listar_tarea, name= 'lista_tarea'),
    path('crear_tarea/', views.crear_tarea, name='crear_tarea'),
    path('eliminar/tarea/<int:id_tarea>', views.eliminar_tarea, name='eliminar_tarea'),
    path('editar/tarea/<int:id_tarea>', views.editar_tarea, name='editar_tarea'),


]