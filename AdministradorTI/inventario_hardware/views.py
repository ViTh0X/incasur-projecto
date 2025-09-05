from django.shortcuts import render
from django.http import Http404

# Create your views here.

def listar_inventario_hardware(request):
    return Http404