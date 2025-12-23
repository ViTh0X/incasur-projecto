from celery import shared_task
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import inventario_software, faltantes_inventario_software,tipo_software
from home.models import logs_actividades_celery
from ips.models import tipo_estado_ips, lista_ips, tipo_equipos_informaticos
from colaboradores.models import lista_colaboradores
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
from utilidades.utilidades_ssh import SSHManager

@shared_task
def ejecutar_inventario_software():
    try:
        estado_ips = get_object_or_404(tipo_estado_ips,pk=1)
        laptop = get_object_or_404(tipo_equipos_informaticos,pk=1)
        pc = get_object_or_404(tipo_equipos_informaticos,pk=2)
        nombres_a_filtrar = [laptop.nombre_tipo_equipo, pc.nombre_tipo_equipo]        
        lista_ips_ocupadas = lista_ips.objects.filter(codigo_estado=estado_ips,tipo_equipo__in=nombres_a_filtrar).values('ip')        
        for ip in lista_ips_ocupadas:
            string_ip = ip['ip']
            username = "Administrador"
            puerto = os.getenv('SSH_PORT')
            keyfile = os.getenv('SSH_KEYFILE')
            passphrase = os.getenv('SSH_PASSPHRASE')
            SSH_instancia = SSHManager(string_ip,username,puerto,keyfile,passphrase)
            esta_en_linea = SSH_instancia.revisarConexionSSH()
            #Filtrando el objeto ip
            ip_filtrada = lista_ips.objects.get(ip=string_ip)
            #Filtrando el objeto nombre Trabajador
            nombre_colab_filtrado = lista_colaboradores.objects.get(ip_colaborador=string_ip)
            print(f"{string_ip} - El equipo esta en linea")            
            mes_actual = datetime.now().month
            año_actual = datetime.now().year                    
            try:
                if esta_en_linea:
                    print(f"Equipo en linea {string_ip}")
                    SSH_instancia.actualizar_ejecutable_software()               
                    print("Actualizacion Finalizada")
                    SSH_instancia.ejecuta_inventario_software()
                    print("Ejecuto inventario software")    
                    inventario_software.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual,ip=ip_filtrada).delete()
                    print("Elimino duplicados")
                    ##################################                    
                    diccionario_inventario_software = SSH_instancia.guardar_inventario_software()                    
                    for codigo_categoria, lista_software in diccionario_inventario_software.items():
                        categoria = tipo_software.objects.get(id=codigo_categoria)
                        for software in lista_software:
                            modelado_inventario_software = inventario_software(
                                ip = ip_filtrada,
                                tipo_software = categoria,
                                nombre_software =software                                
                            )
                            modelado_inventario_software.save()                            
                    print("Crea el inventario en DB")                    
                    faltantes_inventario_software.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual,ip=ip_filtrada).delete()
                    print("Elimino duplicados")
                else:
                    faltantes_inventario_software.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual,ip=ip_filtrada).delete()
                    ip_filtrada = lista_ips.objects.get(ip=string_ip)
                    faltantes_hardware = faltantes_inventario_software(ip=ip_filtrada,nombre_colaborador=nombre_colab_filtrado)
                    faltantes_hardware.save()                      
            except Exception as e:
                print(f"Error {e}")                
                faltantes_inventario_software.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual,ip=ip_filtrada).delete()
                ip_filtrada = lista_ips.objects.get(ip=string_ip)
                faltantes_hardware = faltantes_inventario_software(ip=ip_filtrada,nombre_colaborador=nombre_colab_filtrado)
                faltantes_hardware.save()
        
        logs_inventario_hardware = logs_actividades_celery(            
            mensaje = 'La ejecucion de inventario de software termino sin interrupciones.'
        )                                
        logs_inventario_hardware.save()
        return "TAREA INVENTARIO SOFTWARE TERMINARDA"         
            
    except Exception as e:
        logs_inventario_hardware = logs_actividades_celery(
            mensaje = f"Error {e}"
            # mensaje = 'Ubo un error en la ejecucion de inventario de software no se completo.'
        )                                
        logs_inventario_hardware.save()
        return "ERROR INVENTARIO SOFTWARE"
    

@shared_task
def ejecutar_faltantes_inventario_software():
    try:
        try:
            lista_faltantes = get_list_or_404(faltantes_inventario_software.objects.all())            
        except:
            return "NO HAY FALTANTES TAREA TERMINADA"        
        for ip_faltantes in lista_faltantes:
            string_ip = ip_faltantes.ip.ip
            username = "Administrador"
            puerto = os.getenv('SSH_PORT')
            keyfile = os.getenv('SSH_KEYFILE')
            passphrase = os.getenv('SSH_PASSPHRASE')
            SSH_instancia = SSHManager(string_ip,username,puerto,keyfile,passphrase)
            esta_en_linea = SSH_instancia.revisarConexionSSH()
            #Filtrando el objeto ip
            ip_filtrada = lista_ips.objects.get(ip=string_ip)
            #Filtrando el objeto nombre Trabajador
            nombre_colab_filtrado = lista_colaboradores.objects.get(ip_colaborador=string_ip)            
            mes_actual = datetime.now().month
            año_actual = datetime.now().year                    
            try:
                if esta_en_linea:
                    print(f"Equipo en linea {string_ip}")
                    SSH_instancia.actualizar_ejecutable_software()               
                    print("Actualizacion Finalizada")
                    SSH_instancia.ejecuta_inventario_software()
                    inventario_software.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual,ip=ip_filtrada).delete()
                    print("Elimino Duplicados")
                    diccionario_inventario_software = SSH_instancia.guardar_inventario_software()
                    print("Guardo el Inventario")
                    for codigo_categoria, lista_software in diccionario_inventario_software.items():
                        categoria = tipo_software.objects.get(id=codigo_categoria)
                        for software in lista_software:
                            modelado_inventario_software = inventario_software(
                                ip = ip_filtrada,
                                tipo_software = categoria,
                                nombre_software =software                                
                            )
                            modelado_inventario_software.save()
                    faltantes_inventario_software.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual,ip=ip_filtrada).delete()
                else:
                    faltantes_inventario_software.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual,ip=ip_filtrada).delete()
                    ip_filtrada = lista_ips.objects.get(ip=string_ip)
                    faltantes_hardware = faltantes_inventario_software(ip=ip_filtrada,nombre_colaborador=nombre_colab_filtrado)
                    faltantes_hardware.save()                      
            except Exception as e:
                print(f"Error_ssh {e}")
                faltantes_inventario_software.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual,ip=ip_filtrada).delete()
                ip_filtrada = lista_ips.objects.get(ip=string_ip)
                faltantes_hardware = faltantes_inventario_software(ip=ip_filtrada,nombre_colaborador=nombre_colab_filtrado)
                faltantes_hardware.save()
        
        logs_inventario_hardware = logs_actividades_celery(
            mensaje = 'La ejecucion FALTANTES de inventario de software termino sin interrupciones.'
        )                                
        logs_inventario_hardware.save()
        return "TAREA FALTANTES INVENTARIO SOFTWARE TERMINARDA"         
            
    except Exception as e:
        logs_inventario_hardware = logs_actividades_celery(
            mensaje = f"Error{e}"
            # mensaje = 'Ubo un error en la ejecucion de FALTANTES inventario de software no se completo.'
        )                                
        logs_inventario_hardware.save()
        return "ERROR FALTANTES INVENTARIO SOFTWARE"

@shared_task
def actualizar_ejecutable():
    try:
        estado_ips = get_object_or_404(tipo_estado_ips,pk=1)
        laptop = get_object_or_404(tipo_equipos_informaticos,pk=1)
        pc = get_object_or_404(tipo_equipos_informaticos,pk=2)
        nombres_a_filtrar = [laptop.nombre_tipo_equipo, pc.nombre_tipo_equipo]        
        lista_ips_ocupadas = lista_ips.objects.filter(codigo_estado=estado_ips,tipo_equipo__in=nombres_a_filtrar).values('ip')        
        for ip in lista_ips_ocupadas:
            string_ip = ip['ip']
            username = "Administrador"
            puerto = os.getenv('SSH_PORT')
            keyfile = os.getenv('SSH_KEYFILE')
            passphrase = os.getenv('SSH_PASSPHRASE')            
            SSH_instancia = SSHManager(string_ip,username,puerto,keyfile,passphrase)
            esta_en_linea = SSH_instancia.revisarConexionSSH()
            try:
                if esta_en_linea:
                    print(f"Equipo en linea {string_ip}")
                    SSH_instancia.actualizar_ejecutable_software()               
                    print("Actualizacion Finalizada")                                              
                else:
                    print(f"{string_ip} No esta en linea")
            except Exception as e:
                print(f"{string_ip} No esta en linea")    
        logs_inventario_hardware = logs_actividades_celery(
            mensaje = 'Actualizo los exe de software con exito.'
        )                                
        logs_inventario_hardware.save()
        return "ACTUALIZACION DE EJECUTABLES SOFTWARE TERMINARDA "

    except Exception as e:
        logs_inventario_hardware = logs_actividades_celery(
            mensaje = f"Error{e}"
        )                                
        logs_inventario_hardware.save()
        return "ERROR AL ACTUALIZAR LOS EJECUTABLES SOFTWARE"