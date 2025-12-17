from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class Categorias(models.Model):
    
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre

class Noticias(models.Model):

    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noticias")
    categoria = models.ForeignKey(Categorias, on_delete=models.SET_NULL, null=True)
    titulo = models.CharField(max_length=300)
    contenido =  models.TextField()
    imagen = models.ImageField(upload_to="Images/Media")
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    noticia = models.ForeignKey(Noticias,on_delete=models.CASCADE,related_name="comentarios")
    autor = models.ForeignKey(User,on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.autor} en {self.noticia}"