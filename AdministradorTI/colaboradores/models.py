from django.db import models
from django import forms

#from ips.models import lista_ips

# Create your models here.

'''class cargo_colaboradores(models.Model):
    codigo_cargo = models.AutoField(primary_key=True)
    nombre_cargo = models.CharField(max_length=60)
    
    class Meta:
        db_table = 'cargo_colaboradores'
        
    def __str__(self):
        return self.nombre_cargo'''



class estado_colaboradores(models.Model):
    codigo_estado = models.AutoField(primary_key=True)
    nombre_estado = models.CharField(max_length=20)    
    
    class Meta:
        db_table = 'estado_colaboradores'
    
    def __str__(self):
        return self.nombre_estado


class colaboradores(models.Model):
    codigo_colaborador = models.AutoField(primary_key=True)
    nombre_colaborador = models.CharField(max_length=150,unique=False)
    #ip_colaborador = models.ForeignKey(lista_ips,on_delete=models.CASCADE, to_field='ip')
    usuario_sistema = models.CharField(max_length=25,default='SIN ACCESO AL SISTEMA')
    correo = models.CharField(max_length=50,unique=False)
    usuario_sentinel = models.CharField(max_length=15,default="SIN SENTINEL")
    usuario_sbs = models.CharField(max_length=15,default="SIN SBS")
    usuario_windows = models.CharField(max_length=15,default="SIN WINDOWS")
    usuario_reloj_control = models.CharField(max_length=15,default="SIN MARCACION")
    codigo_impresion_colaborador = models.CharField(max_length=20,unique=False)    
    cargo_colaborador = models.CharField(max_length=70,null=True)    
    estado_colaboradores = models.ForeignKey(estado_colaboradores,on_delete=models.CASCADE)    
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'colaboradores'
    
    def __str__(self):
        return self.nombre_colaborador        


    
class colaboradorForm(forms.ModelForm):
    class Meta:
        model = colaboradores
        fields = ['nombre_colaborador','usuario_sistema','correo','usuario_sentinel','usuario_sbs','usuario_windows','usuario_reloj_control','codigo_impresion_colaborador','cargo_colaborador']
        
class colaboradorForm_editar(forms.ModelForm):
    class Meta:
        model = colaboradores
        fields = ['nombre_colaborador','usuario_sistema','correo','usuario_sentinel','usuario_sbs','usuario_windows','usuario_reloj_control','codigo_impresion_colaborador','cargo_colaborador']