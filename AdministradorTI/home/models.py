from django.db import models

# Create your models here.

class usrforticli(models.Model):
    usuario = models.TextField(max_length=20)
    contrasena = models.TextField(max_length=50)
    usuarioasignado = models.TextField(max_length=200)