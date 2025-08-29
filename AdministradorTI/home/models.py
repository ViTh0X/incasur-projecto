from django.db import models
from colaboradores.models import lista_colaboradores

# Create your models here.

class cuentas_forticlient(models.Model):
    id = models.CharField(primary_key=True)
    usuario = models.CharField(max_length=20,unique=True)
    contraseña = models.TextField(max_length=15,unique=True)
    usuario_asignado = models.ForeignKey(lista_colaboradores,null=True,blank=True,on_delete=models.CASCADE,to_field='nombre_colaborador')
    fecha_modificacion = models.DateField(auto_now=True)
    
    class Meta:
        db_table = 'cuentas_forticlient'
        
    def __str__(self):
        return self.usuario