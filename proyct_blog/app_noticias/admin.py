from django.contrib import admin
from .models import Noticias
from .models import Categorias

# Register your models here.

@admin.register(Noticias)
class NoticiasAdmin(admin.ModelAdmin):
    #AGREGA LOS CAMPOS QUE PASEMOS EN LA TUPLA.
    list_display = ("titulo", "categoria", "fecha")
    #FILTRA LAS (NOTICIAS) POR CATEGORIA
    list_filter = ("categoria",)
    #AGREGA UN CUADRO DE BUSQUEDA POR (CATEGORIA).
    search_fields = ("categoria",)



admin.site.register(Categorias)

