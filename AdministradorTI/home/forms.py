from django import forms
from django.forms import PasswordInput


class Formulario_Login(forms.Form):
    usuario = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Usuario','autocomplete':'off'}))
    password = forms.CharField(required=True,widget=PasswordInput(attrs={'placeholder':'Contraseña','autocomplete':'off'}))