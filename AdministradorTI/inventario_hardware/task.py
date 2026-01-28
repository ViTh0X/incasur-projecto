from celery import shared_task
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import inventario_hardware, faltantes_inventario_hardware
from home.models import logs_actividades_celery
from ips.models import tipo_estado_ips, ips,tipo_equipos_informaticos
#from colaboradores.models import colaboradores
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
from utilidades.utilidades_ssh import SSHManager

@shared_task
def ejecutar_inventario_hardware():
    try:        
        estado_ips = get_object_or_404(tipo_estado_ips,pk=1)
        laptop = get_object_or_404(tipo_equipos_informaticos,pk=1)
        pc = get_object_or_404(tipo_equipos_informaticos,pk=2)
        nombres_a_filtrar = [laptop, pc]        
        lista_ips_ocupadas = ips.objects.filter(codigo_estado=estado_ips,tipo_equipo_asignado__in=nombres_a_filtrar).values('ip')        
        for ip in lista_ips_ocupadas:
            string_ip = ip['ip']
            username = "Administrador"
            puerto = os.getenv('SSH_PORT')
            keyfile = os.getenv('SSH_KEYFILE')
            passphrase = os.getenv('SSH_PASSPHRASE')            
            SSH_instancia = SSHManager(string_ip,username,puerto,keyfile,passphrase)
            #esta_en_linea = SSH_instancia.revisarConexionSSH()
            #Filtrando el objeto ip
            ip_filtrada = ips.objects.get(ip=string_ip)
            #Filtrando el objeto nombre Trabajador
            #nombre_colab_filtrado = ips.objects.get(colaborador_asignado=string_ip)
            mes_actual = datetime.now().month
            año_actual = datetime.now().year
            try:                
                #if esta_en_linea:                
                #SSH_instancia.actualizar_ejecutable_hardware()               
                #print("Actualizacion Finalizada")
                print(f"********TRABAJANDO IP {string_ip}*********")  
                ejecucion_correcta = SSH_instancia.ejecuta_inventario_hardware()               
                if ejecucion_correcta:
                    print("Ejecuto inventario hardware")                                
                    inventario_hardware.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual,codigo_ip=ip_filtrada).delete()
                    print("Elimino duplicados")                    
                    diccionario_inventario_hardware = SSH_instancia.guardar_inventario_hardware()                
                    print("Guardo el inventario")
                    modelado_inventario_hardware = inventario_hardware(
                        codigo_ip = ip_filtrada,
                        codigo_colaborador = ip_filtrada.colaborador_asignado,
                        nombre_equipo = diccionario_inventario_hardware['nombre_pc'],
                        placa = diccionario_inventario_hardware['placa'],
                        procesador = diccionario_inventario_hardware['procesador'],
                        ram = diccionario_inventario_hardware['ram'],
                        video_integrada = diccionario_inventario_hardware['tarjeta_integrada'],
                        video_dedicada = diccionario_inventario_hardware['tarjeta_dedicada'],
                        so = diccionario_inventario_hardware['sistema_operativo'],
                        almacenamiento = diccionario_inventario_hardware['almacenamiento'],
                        puertas_enlace = diccionario_inventario_hardware['puerta_enlace']                             
                    )
                    modelado_inventario_hardware.save()
                    print("Crea el inventario en DB")
                    faltantes_inventario_hardware.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual,codigo_ip=ip_filtrada).delete()                                   
                    print("Elimino duplicados")                                   
                else:
                    faltantes_inventario_hardware.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual,codigo_ip=ip_filtrada).delete()
                    ip_filtrada = ips.objects.get(ip=string_ip)
                    faltantes_hardware = faltantes_inventario_hardware(codigo_ip=ip_filtrada,codigo_colaborador=ip_filtrada.colaborador_asignado)
                    faltantes_hardware.save()
            except Exception as e:
                print(f"Error {e}")
                faltantes_inventario_hardware.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual,codigo_ip=ip_filtrada).delete()
                ip_filtrada = ips.objects.get(ip=string_ip)
                faltantes_hardware = faltantes_inventario_hardware(codigo_ip=ip_filtrada,codigo_colaborador=ip_filtrada.colaborador_asignado)
                faltantes_hardware.save()
        
        logs_inventario_hardware = logs_actividades_celery(
            mensaje = 'La ejecucion de inventario de hardware termino sin interrupciones.'
        )                                
        logs_inventario_hardware.save()
        return "TAREA INVENTARIO HARDWARE TERMINARDA"
    
    except Exception as e:
        logs_inventario_hardware = logs_actividades_celery(
            mensaje = f"Error{e}"
        )                                
        logs_inventario_hardware.save()
        return "ERROR FALTANTES INVENTARIO HARDWARE"                             
                             
@shared_task
def ejecutar_faltantes_inventario_hardware():
    try:
        try:
            año_actual = datetime.now().year
            mes_actual = datetime.now().month    
            lista_faltantes = get_list_or_404(faltantes_inventario_hardware.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual))
        except:
            return "NO HAY FALTANTES TAREA TERMINADA"
        for ip_faltantes in lista_faltantes:
            string_ip = ip_faltantes.codigo_ip.ip
            username = "Administrador"
            puerto = os.getenv('SSH_PORT')
            keyfile = os.getenv('SSH_KEYFILE')
            passphrase = os.getenv('SSH_PASSPHRASE')            
            SSH_instancia = SSHManager(string_ip,username,puerto,keyfile,passphrase)
            #esta_en_linea = SSH_instancia.revisarConexionSSH()
            #Filtrando el objeto ip
            ip_filtrada = ips.objects.get(ip=string_ip)
            #Filtrando el objeto nombre Trabajador
            #nombre_colab_filtrado = lista_colaboradores.objects.get(ip_colaborador=string_ip)
            mes_actual = datetime.now().month
            año_actual = datetime.now().year
            try:
                #if esta_en_linea:
                #print(f"Equipo en linea {string_ip}")
                #SSH_instancia.actualizar_ejecutable_hardware()               
                #print("Actualizacion Finalizada")
                print(f"********TRABAJANDO IP {string_ip}*********")  
                ejecucion_correcta = SSH_instancia.ejecuta_inventario_hardware()               
                if ejecucion_correcta:
                    print("Ejecuto inventario hardware")
                    inventario_hardware.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual,codigo_ip=ip_filtrada).delete()
                    print("Elimino duplicados")
                    diccionario_inventario_hardware = SSH_instancia.guardar_inventario_hardware()
                    print("Guardo el Inventario")                                    
                    modelado_inventario_hardware = inventario_hardware(
                        codigo_ip = ip_filtrada,
                        codigo_colaborador = ip_filtrada.colaborador_asignado,
                        nombre_equipo = diccionario_inventario_hardware['nombre_pc'],
                        placa = diccionario_inventario_hardware['placa'],
                        procesador = diccionario_inventario_hardware['procesador'],
                        ram = diccionario_inventario_hardware['ram'],
                        video_integrada = diccionario_inventario_hardware['tarjeta_integrada'],
                        video_dedicada = diccionario_inventario_hardware['tarjeta_dedicada'],
                        so = diccionario_inventario_hardware['sistema_operativo'],
                        almacenamiento = diccionario_inventario_hardware['almacenamiento'],
                        puertas_enlace = diccionario_inventario_hardware['puerta_enlace']                             
                    )
                    modelado_inventario_hardware.save()
                    print("Guardo Informacion en la BD")
                    faltantes_inventario_hardware.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual,codigo_ip=ip_filtrada).delete()                                   
                else:
                    faltantes_inventario_hardware.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual,codigo_ip=ip_filtrada).delete()
                    ip_filtrada = ips.objects.get(ip=string_ip)
                    faltantes_hardware = faltantes_inventario_hardware(codigo_ip=ip_filtrada,codigo_colaborador=ip_filtrada.colaborador_asignado)
                    faltantes_hardware.save()
            except Exception as e:
                print(f"Error_ssh {e}")
                faltantes_inventario_hardware.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual,codigo_ip=ip_filtrada).delete()
                ip_filtrada = ips.objects.get(ip=string_ip)
                faltantes_hardware = faltantes_inventario_hardware(codigo_ip=ip_filtrada,codigo_colaborador=ip_filtrada.colaborador_asignado)
                faltantes_hardware.save()
        
        logs_inventario_hardware = logs_actividades_celery(
            mensaje = 'La ejecucion de FALTANTES inventario de hardware termino sin interrupciones.'
        )                                
        logs_inventario_hardware.save()
        return "TAREA FALTANTES INVENTARIO HARDWARE TERMINARDA"
    
    except Exception as e:
        logs_inventario_hardware = logs_actividades_celery(
            mensaje = f"Error{e}"
        )                                
        logs_inventario_hardware.save()
        return "ERROR FALTANTES INVENTARIO HARDWARE"        
    
    
@shared_task
def actualizar_ejecutable():
    try:
        estado_ips = get_object_or_404(tipo_estado_ips,pk=1)
        laptop = get_object_or_404(tipo_equipos_informaticos,pk=1)
        pc = get_object_or_404(tipo_equipos_informaticos,pk=2)
        nombres_a_filtrar = [laptop, pc]        
        lista_ips_ocupadas = ips.objects.filter(codigo_estado=estado_ips,tipo_equipo_asignado__in=nombres_a_filtrar).values('ip')        
        for ip in lista_ips_ocupadas:
            string_ip = ip['ip']
            username = "Administrador"
            puerto = os.getenv('SSH_PORT')
            keyfile = os.getenv('SSH_KEYFILE')
            passphrase = os.getenv('SSH_PASSPHRASE')            
            SSH_instancia = SSHManager(string_ip,username,puerto,keyfile,passphrase)
            #esta_en_linea = SSH_instancia.revisarConexionSSH()
            try:
                #if esta_en_linea:
                #print(f"Equipo en linea {string_ip}")
                print(f"********TRABAJANDO IP {string_ip}*********")
                SSH_instancia.actualizar_ejecutable_hardware()               
                print("Actualizacion Finalizada")                                                
                #else:
                #    print(f"{string_ip} No esta en linea")
            except Exception as e:
                print(f"{string_ip} No esta en linea")    
        logs_inventario_hardware = logs_actividades_celery(
            mensaje = 'Actualizo los exe de hardware con exito.'
        )                                
        logs_inventario_hardware.save()
        return "ACTUALIZACION DE EJECUTABLES HARDWARE TERMINARDA"

    except Exception as e:
        logs_inventario_hardware = logs_actividades_celery(
            mensaje = f"Error{e}"
        )                                
        logs_inventario_hardware.save()
        return "ERROR AL ACTUALIZAR LOS EJECUTABLES HARDWARE"