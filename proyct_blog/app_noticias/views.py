from django.shortcuts import render, redirect, get_object_or_404
from .models import Noticias,Categorias
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json
from django.utils import timezone
from django.http.request import HttpRequest
from django.db.models import Q # Importar Q para consultas OR
from django.core.exceptions import PermissionDenied # Importar PermissionDenied
from django.urls import reverse # Importar reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # Paginator
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden


# Create your views here.

# from .models import Noticias
# Noticias.objects.all()
#Objeto.delete()=== Delete FROM Noticias WHERE id=4;


#FUNCIONES (VBF)
#@login_required
def listar_noticias(request):
    noticias = Noticias.objects.all()

    ctx = {
        "noticias":noticias,
        "titulo_pagina":"Ultimas Noticias"
    }
    return render(request, "app_noticias/listar_noticias.html", ctx)
    


#CLASES (VBC) GENERICAS

from django.views.generic import ListView, DeleteView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator



class NoticiasListView(ListView):
    model= Noticias
    template_name = "app_noticias/listar_noticias.html"
    context_object_name = "noticias"



@method_decorator(login_required, name="dispatch")
class NoticiaDetailView(DetailView):
    model = Noticias
    template_name = "app_noticias/detalle_noticia.html"


class NoticiaDeleteView(DeleteView):
    model = Noticias
    template_name = "app_noticias/eliminar_noticia.html"
    success_url = reverse_lazy("listar_noticias")


#ELIMINAR CATEGORIA (VBF)

# from django.shortcuts import get_object_or_404, redirect

# def eliminar_categoria(request, pk):
#     categoria = get_object_or_404(Categorias, pk=pk)

#     if request.method == "POST":
#         categoria.delete()
#         return redirect("listar_noticias")
    
#     return render(request, "categorias/eliminar_categoria.html")


# CLASS (LISTVIEW CATEGORIAS) VBC

# class CategoriasListView(ListView):
#     model= Categorias
#     template_name = "categorias/listar_categorias.html"
#     context_object_name = "categorias2"


def listar_categorias(request):
    categorias = Categorias.objects.all()

    ctx = {
        "categorias":categorias,
        "titulo_pagina":"Categorias Disponibles"
    }
    return render(request, "categorias/listar_categorias.html", ctx)

def noticias_por_categoria(request, pk):
    categoria = get_object_or_404(Categorias, pk=pk)
    noticias = Noticias.objects.filter(categoria=categoria)

    ctx = {
        "categoria": categoria,
        "noticias": noticias
    }
    return render(request, "app_noticias/noticias_por_categoria.html", ctx)


#COMENTARIOS

from .models import Comentario
from .forms import ComentarioForm
from django.contrib.auth.models import Group

@login_required
def agregar_comentario(request, pk):
    noticia = get_object_or_404(Noticias, pk=pk)

    # Solo usuarios registrados o colaboradores
    if not request.user.groups.filter(name__in=["Registrado", "Colaboradores", "Admin"]).exists():
        raise PermissionDenied

    if request.method == "POST":
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.noticia = noticia
            comentario.autor = request.user
            comentario.save()
            return redirect("detalle_noticia", pk=pk)
    else:
        form = ComentarioForm()

    return render(request, "comentarios/agregar_comentario.html", {
        "form": form,
        "noticia": noticia
    })

@login_required
def editar_comentario(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk)

    if not (
        request.user == comentario.autor
        or request.user.groups.filter(name__in=["Admin", "Colaboradores"]).exists()
        or request.user.is_superuser
    ):
        raise PermissionDenied

    if request.method == "POST":
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            return redirect("detalle_noticia", pk=comentario.noticia.pk)
    else:
        form = ComentarioForm(instance=comentario)

    return render(request, "comentarios/editar_comentario.html", {
        "form": form
    })

@login_required
def eliminar_comentario(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk)

    if not (
        request.user == comentario.autor
        or request.user.groups.filter(name__in=["Admin", "Colaboradores"]).exists()
        or request.user.is_superuser
    ):
        raise PermissionDenied

    if request.method == "POST":
        noticia_id = comentario.noticia.pk
        comentario.delete()
        return redirect("detalle_noticia", pk=noticia_id)

    return render(request, "comentarios/eliminar_comentario.html", {
        "comentario": comentario
    })


def filtrar_noticias(request):
    noticias = Noticias.objects.all()
    categorias = Categorias.objects.all()

    # FILTRO POR CATEGORÍA
    categoria_id = request.GET.get("categoria")
    if categoria_id:
        noticias = noticias.filter(categoria_id=categoria_id)

    # ORDENAMIENTO
    orden = request.GET.get("orden")

    if orden == "fecha_asc":
        noticias = noticias.order_by("fecha")
    elif orden == "fecha_desc":
        noticias = noticias.order_by("-fecha")
    elif orden == "az":
        noticias = noticias.order_by("titulo")
    elif orden == "za":
        noticias = noticias.order_by("-titulo")

    ctx = {
        "noticias": noticias,
        "categorias": categorias,
        "categoria_seleccionada": categoria_id,
        "orden_actual": orden,
        "titulo_pagina": "Últimas Noticias"
    }

    return render(request, "app_noticias/filtrar_noticias.html", ctx)

def nosotros(request):

    ctx = {
        "titulo_pagina":"Acerca de nosotros"
    }
    return render(request, "info/nosotros.html", ctx)


def es_colaborador(user):
    return (
        user.is_authenticated and
        (user.groups.filter(name="Colaboradores").exists() or user.is_superuser)
    )

from django.core.exceptions import PermissionDenied
from .forms import NoticiaForm

@login_required
def crear_noticia(request):
    if not es_colaborador(request.user):
        raise PermissionDenied

    if request.method == "POST":
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            noticia = form.save(commit=False)
            noticia.autor = request.user
            noticia.save()
            return redirect("listar_noticias")
    else:
        form = NoticiaForm()

    return render(request, "noticias_adm/crear_noticia.html", {
        "form": form
    })

@login_required
def editar_noticia(request, pk):
    noticia = get_object_or_404(Noticias, pk=pk)

    if not es_colaborador(request.user):
        raise PermissionDenied

    if request.method == "POST":
        form = NoticiaForm(request.POST, request.FILES, instance=noticia)
        if form.is_valid():
            form.save()
            return redirect("detalle_noticia", pk=pk)
    else:
        form = NoticiaForm(instance=noticia)

    return render(request, "noticias_adm/editar_noticia.html", {
        "form": form
    })

@login_required
def eliminar_noticia(request, pk):
    noticia = get_object_or_404(Noticias, pk=pk)

    if not es_colaborador(request.user):
        raise PermissionDenied

    if request.method == "POST":
        noticia.delete()
        return redirect("listar_noticias")

    return render(request, "noticias_adm/eliminar_noticia.html", {
        "noticia": noticia
    })


#CATEGORIAS_ADM

from .forms import CategoriaForm


@login_required
def crear_categoria(request):
    if not es_colaborador(request.user):
        raise PermissionDenied

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        if nombre:
            Categorias.objects.create(nombre=nombre)
            return redirect("listar_categorias")
        
    return render(request, "categorias/crear_categoria.html")

# @login_required
# def editar_categoria(request, pk):
#     categoria = get_object_or_404(Categorias, pk=pk)

#     if not es_colaborador(request.user):
#         raise PermissionDenied
     
#     if request.method == "POST":
#         categoria.nombre = request.POST.get("nombre")
#         categoria.save()
#     return redirect("listar_categorias")


@login_required
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categorias, pk=pk)

    if not es_colaborador(request.user):
        raise PermissionDenied

    if request.method == "POST":
        categoria.nombre = request.POST.get("nombre")
        categoria.save()
        return redirect("listar_categorias")

    return render(request, "categorias/editar_categoria.html", {
        "categoria": categoria
    })

#     return render(request, "categorias/editar_categoria.html", {
#         "categoria": categoria
#     })

# def eliminar_categoria(request, pk):
#     categoria = get_object_or_404(Categorias, pk=pk)

#     if request.method == "POST":
#         categoria.delete()
#         return redirect("listar_noticias")
    
#     return render(request, "categorias/eliminar_categoria.html")


@login_required
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categorias, pk=pk)

    if not es_colaborador(request.user):
        raise PermissionDenied

    if request.method == "POST":
        categoria.delete()
        return redirect("listar_categorias")

    return render(request, "categorias/eliminar_categoria.html", {
        "categoria": categoria
    })