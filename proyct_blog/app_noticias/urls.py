
from django.urls import path
from . import views
from .views import NoticiasListView, NoticiaDetailView, NoticiaDeleteView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #URL PARA VISTA EN FUNCIONES
     path("noticias/", views.listar_noticias, name="listar_noticias"),
        #URL PARA VISTA EN CLASES
    #  path("noticias2/", NoticiasListView.as_view(), name="listar_noticias"),
     path("detalle_noticia/<int:pk>", NoticiaDetailView.as_view(), name="detalle_noticia"),
     path("eliminar_noticia/<int:pk>", NoticiaDeleteView.as_view()),
     #URL CATEGORIA FUNCION
    # path("eliminar_categoria/<int:pk>", views.eliminar_categoria),
        # CATEGORÍAS
    path("categorias2/", views.listar_categorias, name="listar_categorias"),
    path("categoria/<int:pk>/", views.noticias_por_categoria, name="noticias_por_categoria"),
    path("categorias2/crear/", views.crear_categoria, name="crear_categoria"),
    path("categorias2/editar/<int:pk>/", views.editar_categoria, name="editar_categoria"),
    path("categorias2/eliminar/<int:pk>/", views.eliminar_categoria, name="eliminar_categoria"),
        #INFO_ADMIN
    path("nosotros/", views.nosotros, name="nosotros"),
        #COMENTARIOS
    path("comentario/agregar/<int:pk>/", views.agregar_comentario, name="agregar_comentario"),
    path("comentario/editar/<int:pk>/", views.editar_comentario, name="editar_comentario"),
    path("comentario/eliminar/<int:pk>/", views.eliminar_comentario, name="eliminar_comentario"),
        #NOTICIAS_ADM
    path("noticias_por/", views.filtrar_noticias, name="filtrar_noticias"),
    path("noticia/crear/", views.crear_noticia, name="crear_noticia"),
    path("noticia/editar/<int:pk>/", views.editar_noticia, name="editar_noticia"),
    path("noticia/eliminar/<int:pk>/", views.eliminar_noticia, name="eliminar_noticia"),
]   

