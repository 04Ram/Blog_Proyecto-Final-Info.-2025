from django import forms
from .models import Comentario

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ["contenido"]
        widgets = {
            "contenido": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Escribe tu comentario..."
            })
        }


from .models import Noticias

class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticias
        fields = ["titulo", "contenido", "imagen", "categoria"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "contenido": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
            "categoria": forms.Select(attrs={"class": "form-select"}),
        }


from .models import Categorias

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categorias  
        fields = ["nombre"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class":"form-control"})
        }