from django.contrib.auth.forms import UserCreationForm

#MODELO POR DEFECTO DE USUARIOS "DJANGO"
from django.contrib.auth.models import User
from django import forms

class PersonalizadoUserCreationForm(UserCreationForm):

    email = forms.EmailField(required=True, help_text="Campo Obligatorio.")

    class Meta:
        model = User
        fields = ("username", "email")


