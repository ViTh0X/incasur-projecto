from django.db import models

# Create your models here.

class tipo_estado_ips(models.Model):
    codigo_estado = models.AutoField(primary_key=True)
    nombre_estado = models.CharField(max_length=40,unique=True)
    descripcion_estado = models.CharField(max_length=60)
    
    class Meta:
        db_table = 'tipo_estado_ips'
        
    def __str__(self):
        return self.codigo_estado
    
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
        
class lista_ips(models.Model):  
    id = models.CharField(primary_key=True)  
    ip = models.CharField(max_length=15,unique=True) 
    ip_seccion = models.ForeignKey(tipo_secciones,on_delete=models.CASCADE,null=True,blank=True,to_field='nombre_seccion')
    ip_nivel_firewall = models.ForeignKey(niveles_firewall,on_delete=models.CASCADE,null=True,blank=True,to_field='nombre_nivel')    
    tipo_equipo = models.ForeignKey(tipo_equipos_informaticos,on_delete=models.CASCADE,null=True,blank=True,to_field='nombre_tipo_equipo')    
    marca_equipo = models.CharField(default='Generico',max_length=120)
    modelo_equipo = models.CharField(default='Generico',max_length=120)
    oficina = models.ForeignKey(oficinas,on_delete=models.CASCADE,null=True,blank=True,to_field='nombre_oficina')
    codigo_estado = models.ForeignKey(tipo_estado_ips,on_delete=models.CASCADE,null=True,blank=True,to_field='nombre_estado')
    fecha_modificacion = models.DateField(auto_now=True)
    
    class Meta:
        db_table = 'lista_ips'
        # Ordena los resultados por el campo 'ip' de forma ascendente
        ordering = ['id']
        
    def __str__(self):
        return self.ip
    