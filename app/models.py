from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):  
    ADMINISTRADOR = 1
    USUARIO = 2

    ROLES = (
        (ADMINISTRADOR, 'Administrador'),
        (USUARIO, 'Usuario'),
    )

    rol = models.PositiveSmallIntegerField(choices=ROLES, default=USUARIO)
    telefono = models.CharField(max_length=20, blank=True, null=True)


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(
        'Usuario', on_delete=models.CASCADE, related_name='categorias'
    )


class Proyecto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateField(blank=True, null=True)
    usuario = models.ForeignKey(
        'Usuario', on_delete=models.CASCADE, related_name='proyectos'
    )


class Tarea(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En progreso'),
        ('completada', 'Completada'),
    ]

    PRIORIDAD = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    ]

    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD, default='media')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    completada = models.BooleanField(default=False)

    proyecto = models.ForeignKey(
        Proyecto, on_delete=models.CASCADE, related_name='tareas', null=True, blank=True
    )
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='tareas'
    )
    usuario = models.ForeignKey(
        'Usuario', on_delete=models.CASCADE, related_name='tareas'
    )


class Subtarea(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    completada = models.BooleanField(default=False)
    tarea = models.ForeignKey(
        Tarea, on_delete=models.CASCADE, related_name='subtareas'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)