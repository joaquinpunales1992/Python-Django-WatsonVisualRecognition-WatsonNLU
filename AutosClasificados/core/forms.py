from django import forms
from django.forms import Textarea, TextInput, IntegerField

from .models import Articulo


class FormularioArticulo(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ('titulo', 'marca', 'precio', 'descripcion', 'imagen' )
        widgets = {
            'descripcion': Textarea(attrs={'cols': 51, 'rows': 6}),
            'titulo': TextInput(attrs={'size': 2})


        }

