from django.db import models
from django import forms
# Create your models here.
from colaboradores.models import colaboradores

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

class switches(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150,unique=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'switches'
        
    def __str__(self):
        return self.nombre
    
    
class vlans(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150,unique=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'vlans'
        
    def __str__(self):
        return self.nombre

        
class ips(models.Model):  
    id = models.AutoField(primary_key=True)  
    ip = models.CharField(max_length=15,unique=True)
    #Agregar nuevo campo Roll Asignado
    roll_ip = models.CharField(max_length=120,null=True,blank=True)
    #Agregar codigo de colaborador Asignado
    colaborador_asignado = models.ForeignKey(colaboradores,on_delete=models.CASCADE,null=True,blank=True)
    seccion = models.ForeignKey(tipo_secciones,on_delete=models.CASCADE,null=True,blank=True)
    nivel_firewall = models.ForeignKey(niveles_firewall,on_delete=models.CASCADE,null=True,blank=True)    
    tipo_equipo_asignado = models.ForeignKey(tipo_equipos_informaticos,on_delete=models.CASCADE,null=True,blank=True)    
    marca_equipo_asignado = models.CharField(max_length=120,null=True,blank=True)
    modelo_equipo_asignado = models.CharField(max_length=120,null=True,blank=True)
    oficina = models.ForeignKey(oficinas,on_delete=models.CASCADE,null=True,blank=True)
    codigo_estado = models.ForeignKey(tipo_estado_ips,on_delete=models.CASCADE,null=True,blank=True)
    vlan = models.ForeignKey(vlans,on_delete=models.CASCADE,null=True,blank=True)
    switch = models.ForeignKey(switches,on_delete=models.CASCADE,null=True,blank=True)
    puerto = models.CharField(max_length=3)
    mac = models.CharField(max_length=200)
    fecha_modificacion = models.DateField(auto_now=True)
    
    
    class Meta:
        db_table = 'ips'
        # Ordena los resultados por el campo 'ip' de forma ascendente
        ordering = ['id']
        
    def __str__(self):
        return self.ip
    
class equipos_informaticos_ti(models.Model):  
    id = models.AutoField(primary_key=True)  
    ip = models.CharField(max_length=15,unique=True)    
    roll_ip = models.CharField(max_length=120,null=True,blank=True)    
    colaborador_asignado = models.ForeignKey(colaboradores,on_delete=models.CASCADE,null=True,blank=True)
    seccion = models.ForeignKey(tipo_secciones,on_delete=models.CASCADE,null=True,blank=True)
    nivel_firewall = models.ForeignKey(niveles_firewall,on_delete=models.CASCADE,null=True,blank=True)    
    tipo_equipo_asignado = models.ForeignKey(tipo_equipos_informaticos,on_delete=models.CASCADE,null=True,blank=True)    
    marca_equipo_asignado = models.CharField(max_length=120,null=True,blank=True)
    modelo_equipo_asignado = models.CharField(max_length=120,null=True,blank=True)
    oficina = models.ForeignKey(oficinas,on_delete=models.CASCADE,null=True,blank=True)
    codigo_estado = models.ForeignKey(tipo_estado_ips,on_delete=models.CASCADE,null=True,blank=True)
    vlan = models.ForeignKey(vlans,on_delete=models.CASCADE,null=True,blank=True)
    switch = models.ForeignKey(switches,on_delete=models.CASCADE,null=True,blank=True)
    puerto = models.CharField(max_length=3)
    mac = models.CharField(max_length=200)
    
    placa = models.CharField(max_length=100,blank=True,null=True)
    procesador = models.CharField(max_length=100,blank=True,null=True)
    ram = models.CharField(max_length=6,blank=True,null=True)
    video_integrada = models.CharField(max_length=100,blank=True,null=True)
    video_dedicada = models.CharField(max_length=100,blank=True,null=True)
    so = models.CharField(max_length=20,blank=True,null=True)
    almacenamiento = models.CharField(max_length=200,null=True,blank=True)
    fecha_modificacion = models.DateField(auto_now=True)
        
    class Meta:
        db_table = 'equipos_informaticos_ti'
        # Ordena los resultados por el campo 'ip' de forma ascendente
        ordering = ['id']
        
    def __str__(self):
        return self.ip
    
    
class historial_acciones(models.Model):
    id = models.AutoField(primary_key=True)
    ip_historial = models.CharField(max_length=20)
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
        fields = ['ip','roll_ip','colaborador_asignado','seccion','nivel_firewall','tipo_equipo_asignado','marca_equipo_asignado','modelo_equipo_asignado','oficina','codigo_estado','vlan','switch','puerto','mac']            
        
    def __init__(self, *args,**kwargs)    :
        super().__init__(*args,**kwargs)
        
        if 'tipo_equipo_asignado' in self.fields:
            self.fields['tipo_equipo_asignado'].queryset =self.fields['tipo_equipo_asignado'].queryset.filter(id__in=[1,2]) 
        
    
class EquiposInformaticosForm(forms.ModelForm):
    class Meta:
        model = equipos_informaticos_ti
        fields = ['ip','roll_ip','colaborador_asignado','seccion','nivel_firewall','tipo_equipo_asignado','marca_equipo_asignado','modelo_equipo_asignado','oficina','codigo_estado','vlan','switch','puerto','mac','placa','procesador','ram','video_integrada','video_dedicada','so','almacenamiento']            
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'colaborador_asignado' in self.fields:
            self.fields['colaborador_asignado'].queryset = self.fields['colaborador_asignado'].queryset.exclude(estado_colaboradores=2)
            
            
        if 'tipo_equipo_asignado' in self.fields:
            self.fields['tipo_equipo_asignado'].queryset = self.fields['tipo_equipo_asignado'].queryset.exclude(id__in=[1,2])