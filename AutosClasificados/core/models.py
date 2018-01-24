from __future__ import unicode_literals

from django.db import models


class Articulo(models.Model):
    titulo = models.CharField(max_length=50, blank=True)
    BMW = 'bmw'
    CHEVROLET = 'chevrolet'
    FORD = 'ford'
    NISSAN = 'nissan'
    VOLKSWAGEN = 'volkswagen'
    marca_opciones = (
              (BMW, 'BMW'),
              (CHEVROLET, 'Chevrolet'),
              (FORD, 'Ford'),
              (VOLKSWAGEN, 'Chevrolet'),
              (NISSAN, 'Nissan')
              )
    marca = models.CharField(max_length=20, choices=marca_opciones, default=BMW, blank=True)
    precio = models.IntegerField(blank=True, default=0)
    descripcion = models.TextField(max_length=255, blank=True)
    imagen = models.FileField(upload_to='documents/')
    fechaPublicacion = models.DateTimeField(auto_now_add=True)
    resWatsonClase = models.CharField(max_length=1000, blank=True, null=True)
    resWatsonScore = models.IntegerField(blank=True, null=True)
    resWatsonValidacionMarca = models.IntegerField(blank=True, null=True)
    resWatsonClasificacionDescripcion = models.CharField(max_length=110, blank=True, null=True)





