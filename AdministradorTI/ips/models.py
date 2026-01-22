from django.db import models
from django import forms
# Create your models here.
from colaboradores.models import lista_colaboradores

class tipo_estado_ips(models.Model):
    codigo_estado = models.AutoField(primary_key=True)
    nombre_estado = models.CharField(max_length=40,unique=True)
    descripcion_estado = models.CharField(max_length=60)
    
    class Meta:
        db_table = 'tipo_estado_ips'
        
    def __str__(self):
        return self.nombre_estado
    
class tipo_secciones(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_seccion = models.CharField(max_length=50,unique=True)
    descripcion_seccion = models.CharField(max_length=120)
    
    class Meta:
        db_table = 'tipo_secciones'

    def __str__(self):
        return self.nombre_seccion
    
class niveles_firewall(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_nivel = models.CharField(max_length=50,unique=True)
    descripcion_nivel = models.CharField(max_length=120)
    
    class Meta:
        db_table = 'niveles_firewall'
        
    def __str__(self):
        return self.nombre_nivel
    
class tipo_equipos_informaticos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_tipo_equipo = models.CharField(max_length=50,unique=True)
    descripcion_tipo_equipo = models.CharField(max_length=120)
    
    class Meta:
        db_table = 'tipo_equipos_informaticos'
        
    def __str__(self):
        return self.nombre_tipo_equipo
    
class oficinas(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_oficina = models.CharField(max_length=150,unique=True)
    
    class Meta:
        db_table = 'oficinas'
        
    def __str__(self):
        return self.nombre_oficina    
        
class ips(models.Model):  
    id = models.AutoField(primary_key=True)  
    ip = models.CharField(max_length=15,unique=True)
    #Agregar nuevo campo Roll Asignado
    roll_ip = models.CharField(max_length=120,null=True,blank=True)
    #Agregar codigo de colaborador Asignado
    colaborador_asignado = models.ForeignKey(lista_colaboradores,on_delete=models.CASCADE,null=True,blank=True)
    seccion = models.ForeignKey(tipo_secciones,on_delete=models.CASCADE,null=True,blank=True)
    nivel_firewall = models.ForeignKey(niveles_firewall,on_delete=models.CASCADE,null=True,blank=True)    
    tipo_equipo_asignado = models.ForeignKey(tipo_equipos_informaticos,on_delete=models.CASCADE,null=True,blank=True)    
    marca_equipo_asignado = models.CharField(max_length=120,null=True,blank=True)
    modelo_equipo_asignado = models.CharField(max_length=120,null=True,blank=True)
    oficina = models.ForeignKey(oficinas,on_delete=models.CASCADE,null=True,blank=True)
    codigo_estado = models.ForeignKey(tipo_estado_ips,on_delete=models.CASCADE,null=True,blank=True)
    fecha_modificacion = models.DateField(auto_now=True)
    
    class Meta:
        db_table = 'ips'
        # Ordena los resultados por el campo 'ip' de forma ascendente
        ordering = ['id']
        
    def __str__(self):
        return self.ip
    
class historial_acciones(models.Model):
    id = models.AutoField(primary_key=True)
    ip_historial = models.ForeignKey(ips,on_delete=models.CASCADE)
    nombre_colaborador = models.CharField(max_length=150)
    accion_realizada = models.TextField(max_length=500)
    fecha_realizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'historial_acciones'
        ordering = ['id']
    
    def __str__(self):
        return self.ip
    
class historial_accionForm(forms.ModelForm):
    class Meta:
        model = historial_acciones
        fields = ['ip_historial','accion_realizada'] #Solo van los campos editables "EN HTML" si se editan en el view no es necesario
    
    
class ipForm(forms.ModelForm):
    class Meta:
        model = ips
        fields = ['ip','roll_ip','colaborador_asignado','seccion','ip_nivel_firewall','tipo_equipo_asignado','marca_equipo_asignado','modelo_equipo_asignado','oficina','codigo_estado']            