from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .forms import PersonalizadoUserCreationForm

#REGISTRO (VBF)
def registro_view(request):

    if request.method == "POST":

        form = PersonalizadoUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            messages.success(request, "Usuario Creado.")
            return redirect("login")
        else:
            messages.error(request, "Usuario no creado.")
    
    else:
        form = PersonalizadoUserCreationForm()
    
    return render(request, "app_usuarios/registro.html", {"form":form})


def login_view(request):

    if request.user.is_authenticated:
        return redirect("listar_noticias")
    
    if request.method=="POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Inicio de sesión exitoso.")
                return redirect("listar_noticias")
            else:
                messages.error(request, "Fallo al iniciar sesión.")
        else:
            messages.error(request, "Formulario incorrecto.")
    else:
        form = AuthenticationForm()
    return render(request, "app_usuarios/login.html", {"form":form})


def logout_view(request):
    logout(request)
    return redirect("listar_noticias")
