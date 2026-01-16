from celery import shared_task
from django.shortcuts import get_list_or_404, get_object_or_404
from .models import lista_backups_informacion, faltantes_backup_informacion
from home.models import logs_actividades_celery
from ips.models import tipo_estado_ips, lista_ips,tipo_equipos_informaticos
from colaboradores.models import lista_colaboradores
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
from utilidades.utilidades_ssh import SSHManager

@shared_task()
def ejecutar_backup_informacion():
    try:
        estado_ips = get_object_or_404(tipo_estado_ips,pk=1)
        laptop = get_object_or_404(tipo_equipos_informaticos,pk=1)
        pc = get_object_or_404(tipo_equipos_informaticos,pk=2)
        nombres_a_filtrar = [laptop.nombre_tipo_equipo, pc.nombre_tipo_equipo]        
        lista_ips_ocupadas = lista_ips.objects.filter(codigo_estado=estado_ips,tipo_equipo__in=nombres_a_filtrar).values('ip')
        print(lista_ips_ocupadas)
        for ip in lista_ips_ocupadas:
            string_ip = ip['ip']
            username = "Administrador"
            puerto = os.getenv('SSH_PORT')
            keyfile = os.getenv('SSH_KEYFILE')
            passphrase = os.getenv('SSH_PASSPHRASE')
            SSH_instancia = SSHManager(string_ip,username,puerto,keyfile,passphrase)
            #esta_en_linea = SSH_instancia.revisarConexionSSH()
            #Filtrando el objeto ip
            ip_filtrada = lista_ips.objects.get(ip=string_ip)
            mes_actual = datetime.now().month
            año_actual = datetime.now().year
            lista_backups_informacion.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual,ip=ip_filtrada).delete()
            #Filtrando el objeto nombre Trabajador
            nombre_colab_filtrado = lista_colaboradores.objects.get(ip_colaborador=string_ip)                        
            try:
                #if esta_en_linea:
                equipo_conectado = SSH_instancia.realizarConSSH()
                if equipo_conectado:
                    SSH_instancia.crearCanalSFTP()                    
                    listaRutasLocales = SSH_instancia.rutasIniciales(["Discos"])
                    listaRutas = SSH_instancia.creaRutasRemotas(username,listaRutasLocales,string_ip)
                    print("Inicio la ejecucion del Backup Espere...")
                    for rutas in listaRutas:
                        llave, valor = list(rutas.items())[0]
                        SSH_instancia.realizarBKUP(str(valor),str(llave),"")
                    print("Termino La ejecucion del Backup")
                    SSH_instancia.cerrarConexiones()                    
                    existen_errores = SSH_instancia.verificar_archivos_logs(host=string_ip)
                    if existen_errores:
                        detalle_backup = "Parece que aparecieron unos errores revise el log."                        
                    else:
                        detalle_backup = "El backup termino exitosamente sin errores."
                    modelado_backup_informacion = lista_backups_informacion(
                        ip = ip_filtrada,
                        nombre_colaborador = nombre_colab_filtrado,
                        detalle = detalle_backup
                    )                    
                    modelado_backup_informacion.save()
                    faltantes_backup_informacion.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual,ip=ip_filtrada).delete()
                else:
                    faltantes_backup_informacion.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual,ip=ip_filtrada).delete()
                    ip_filtrada = lista_ips.objects.get(ip=string_ip)
                    faltantes_hardware = faltantes_backup_informacion(ip=ip_filtrada,nombre_colaborador=nombre_colab_filtrado)
                    faltantes_hardware.save()
            except Exception as e:
                print(f"Error_ssh {e}")
                faltantes_backup_informacion.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual,ip=ip_filtrada).delete()
                ip_filtrada = lista_ips.objects.get(ip=string_ip)
                faltantes_hardware = faltantes_backup_informacion(ip=ip_filtrada,nombre_colaborador=nombre_colab_filtrado)
                faltantes_hardware.save()
                
        logs_inventario_hardware = logs_actividades_celery(            
            mensaje = 'La ejecucion de backup de informacion termino sin interrupciones.'
        )                                
        logs_inventario_hardware.save()
        return "TAREA BACKUP DE INFORMACION TERMINARDA"
    except Exception as e:
        logs_inventario_hardware = logs_actividades_celery(
            mensaje = f"Error{e}"
            # mensaje = 'Ubo un error en la ejecucion de inventario de hardware no se completo.'
        )                                
        logs_inventario_hardware.save()
        return "ERROR REALIZANDO EL BACKUP DE INFORMACION"
    
@shared_task()
def ejecutar_faltantes_backup_informacion():
    try:
        try:
            año_actual = datetime.now().year
            mes_actual = datetime.now().month
            lista_faltantes = get_list_or_404(faltantes_backup_informacion.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual))            
        except:
            return "NO HAY FALTANTES TAREA TERMINADA"
        for ip_faltantes in lista_faltantes:
            string_ip = ip_faltantes.ip.ip
            username = "Administrador"
            puerto = os.getenv('SSH_PORT')
            keyfile = os.getenv('SSH_KEYFILE')
            passphrase = os.getenv('SSH_PASSPHRASE')
            SSH_instancia = SSHManager(string_ip,username,puerto,keyfile,passphrase)
            #esta_en_linea = SSH_instancia.revisarConexionSSH()
            #Filtrando el objeto ip
            ip_filtrada = lista_ips.objects.get(ip=string_ip)
            #Filtrando el objeto nombre Trabajador
            nombre_colab_filtrado = lista_colaboradores.objects.get(ip_colaborador=string_ip)
            mes_actual = datetime.now().month
            año_actual = datetime.now().year
            try:
                #if esta_en_linea:
                equipo_conectado = SSH_instancia.realizarConSSH()
                if equipo_conectado:
                    SSH_instancia.crearCanalSFTP()
                    lista_backups_informacion.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual,ip=ip_filtrada).delete()
                    listaRutasLocales = SSH_instancia.rutasIniciales(["Documentos","Escritorio","Descargas","Discos"])
                    listaRutas = SSH_instancia.creaRutasRemotas(username,listaRutasLocales)
                    for rutas in listaRutas:
                        llave, valor = list(rutas.items())[0]
                        SSH_instancia.realizarBKUP(str(valor),str(llave),"")
                    SSH_instancia.cerrarConexiones()
                    existen_errores = SSH_instancia.verificar_archivos_logs(host=string_ip)
                    if existen_errores:
                        detalle_backup = "Parece que aparecieron unos errores revise el log."                        
                    else:
                        detalle_backup = "El backup termino exitosamente sin errores."
                    modelado_backup_informacion = lista_backups_informacion(
                        ip = ip_filtrada,
                        nombre_colaborador = nombre_colab_filtrado,
                        detalle = detalle_backup
                    )
                    modelado_backup_informacion.save()
                    faltantes_backup_informacion.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual,ip=ip_filtrada).delete()
                else:
                    faltantes_backup_informacion.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual,ip=ip_filtrada).delete()
                    ip_filtrada = lista_ips.objects.get(ip=string_ip)
                    faltantes_hardware = faltantes_backup_informacion(ip=ip_filtrada,nombre_colaborador=nombre_colab_filtrado)
                    faltantes_hardware.save()
                
            except Exception as e:
                print(f"Error_ssh {e}")
                faltantes_backup_informacion.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual,ip=ip_filtrada).delete()
                ip_filtrada = lista_ips.objects.get(ip=string_ip)
                faltantes_hardware = faltantes_backup_informacion(ip=ip_filtrada,nombre_colaborador=nombre_colab_filtrado)
                faltantes_hardware.save()
        
        logs_inventario_hardware = logs_actividades_celery(            
            mensaje = 'La ejecucion de FALTANTES backup de informacion termino sin interrupciones.'
        )                                
        logs_inventario_hardware.save()
        return "TAREA FALTANTES BACKUP DE INFORMACION TERMINARDA"
    
    except Exception as e:
        logs_inventario_hardware = logs_actividades_celery(
            mensaje = f"Error{e}"
            # mensaje = 'Ubo un error en la ejecucion de FALTANTES inventario de software no se completo.'
        )                                
        logs_inventario_hardware.save()
        return "ERROR REALIZANDO EL FALTANTES BACKUP DE INFORMACION"        


@shared_task()
def ejecutar_backup_individual(ip):
    try:
        username = "Administrador"
        puerto = os.getenv('SSH_PORT')
        keyfile = os.getenv('SSH_KEYFILE')
        passphrase = os.getenv('SSH_PASSPHRASE')
        SSH_instancia = SSHManager(ip,username,puerto,keyfile,passphrase)
        #esta_en_linea = SSH_instancia.revisarConexionSSH()
        #Filtrando el objeto ip
        ip_filtrada = lista_ips.objects.get(ip=ip)
        mes_actual = datetime.now().month
        año_actual = datetime.now().year
        lista_backups_informacion.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual,ip=ip_filtrada).delete()
        #Filtrando el objeto nombre Trabajador
        nombre_colab_filtrado = lista_colaboradores.objects.get(ip_colaborador=ip)                        
        try:
            #if esta_en_linea:
            equipo_conectado = SSH_instancia.realizarConSSH()
            if equipo_conectado:
                SSH_instancia.crearCanalSFTP()                    
                listaRutasLocales = SSH_instancia.rutasIniciales(["Discos"])
                listaRutas = SSH_instancia.creaRutasRemotas(username,listaRutasLocales,ip)
                print("Inicio la ejecucion del Backup Espere...")
                for rutas in listaRutas:
                    llave, valor = list(rutas.items())[0]
                    SSH_instancia.realizarBKUP(str(valor),str(llave),"")
                print("Termino La ejecucion del Backup")
                SSH_instancia.cerrarConexiones()                    
                existen_errores = SSH_instancia.verificar_archivos_logs(host=ip)
                if existen_errores:
                    detalle_backup = "Parece que aparecieron unos errores revise el log."                        
                else:
                    detalle_backup = "El backup termino exitosamente sin errores."
                modelado_backup_informacion = lista_backups_informacion(
                    ip = ip_filtrada,
                    nombre_colaborador = nombre_colab_filtrado,
                    detalle = detalle_backup
                )                    
                modelado_backup_informacion.save()
                faltantes_backup_informacion.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual,ip=ip_filtrada).delete()
            else:
                faltantes_backup_informacion.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual,ip=ip_filtrada).delete()
                ip_filtrada = lista_ips.objects.get(ip=ip)
                faltantes_hardware = faltantes_backup_informacion(ip=ip_filtrada,nombre_colaborador=nombre_colab_filtrado)
                faltantes_hardware.save()
        except Exception as e:
            print(f"Error_ssh {e}")
            faltantes_backup_informacion.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual,ip=ip_filtrada).delete()
            ip_filtrada = lista_ips.objects.get(ip=ip)
            faltantes_hardware = faltantes_backup_informacion(ip=ip_filtrada,nombre_colaborador=nombre_colab_filtrado)
            faltantes_hardware.save()
        
        logs_inventario_hardware = logs_actividades_celery(            
            mensaje = f'La ejecucion de {ip} backup de informacion termino sin interrupciones.'
        )                                
        logs_inventario_hardware.save()
        return f"TAREA BACKUP {ip} DE INFORMACION TERMINARDA"
    except Exception as e:
        logs_inventario_hardware = logs_actividades_celery(
            mensaje = f"Error{e}"
            # mensaje = 'Ubo un error en la ejecucion de inventario de hardware no se completo.'
        )                                
        logs_inventario_hardware.save()
        return f"ERROR REALIZANDO EL BACKUP DE INFORMACION {ip}"    
