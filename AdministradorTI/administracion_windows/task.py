from celery import shared_task
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import EstadoAccionesWindows, FaltantesRevisionEquiposWindows
from ips.models import ips,tipo_estado_ips,tipo_equipos_informaticos
from colaboradores.models import colaboradores
import os
from datetime import datetime
from utilidades.utilidades_ssh import SSHManager

lista_acceso_total = ['Gerente General','Gerente Comercial','Gerente De TI','Gerente De Auditoria Interna','Gerente De Riesgos','Gerente De Investigación, Desarrollo E Innovacion','Gerente De Administracion Y Finanzas','Jefe De Marketing E Inteligencia Comercial','Asistente De Rrhh Y Logistica','Asistente de Producción']
lista_solo_lectura = ['Jefe De Operaciones Central','Jefe De Productos Negocios','Asistente De Finanzas']
ip_cajas = ['192.168.1.56','192.168.1.57']

@shared_task
def verificacion_usb_all():
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
            ip_filtrada = ips.objects.get(ip=string_ip)            
            windows_actualizacion = EstadoAccionesWindows.objects.get(id_ip=ip_filtrada.id)                     
            try:                                
                print(f"********TRABAJANDO IP {string_ip}*********")  
                estado_puertos = SSH_instancia.estatus_puerto_usb()                                                
                print(estado_puertos)                 
                if not estado_puertos == "Error al consultar":                                                                                                              
                    FaltantesRevisionEquiposWindows.objects.filter(codigo_ip=ip_filtrada).delete()
                    if ip_filtrada.colaborador_asignado.cargo_colaborador.nombre_cargo in lista_acceso_total:
                        if estado_puertos.lower().strip() == 'disponible':
                            windows_actualizacion.estado_puertos_usb = "Acceso Total"
                            windows_actualizacion.save()
                        else:
                            print("Trantando de cambiarlo segun politica")
                            try:
                                resultado = SSH_instancia.ejecutar_desbloqueo_total_usb()                            
                                windows_actualizacion.estado_puertos_usb = "Acceso Total"
                                windows_actualizacion.estato_actualizacion = resultado
                                windows_actualizacion.save()
                            except:
                                windows_actualizacion.estato_actualizacion = "No Actualizado"
                                windows_actualizacion.save()
                    elif ip_filtrada.colaborador_asignado.cargo_colaborador.nombre_cargo in lista_solo_lectura or ip_filtrada.ip in ip_cajas:
                        if estado_puertos.lower().strip() == 'solo lectura':
                            windows_actualizacion.estado_puertos_usb = "Solo Lectura"
                            windows_actualizacion.save()
                        else:
                            print("Trantando de cambiarlo segun politica")
                            try:
                                resultado = SSH_instancia.ejecutar_cambiar_usb_solo_lectura()                            
                                windows_actualizacion.estado_puertos_usb = "Solo Lectura"
                                windows_actualizacion.estato_actualizacion = resultado
                                windows_actualizacion.save()
                            except:
                                windows_actualizacion.estato_actualizacion = "No Actualizado"
                                windows_actualizacion.save()
                    else:                                   
                        if estado_puertos.lower().strip() == 'bloqueado':
                            windows_actualizacion.estado_puertos_usb = "Bloqueado"
                            windows_actualizacion.save()
                        else:
                            print("Trantando de cambiarlo segun politica")
                            try:
                                resultado = SSH_instancia.ejecutar_bloqueo_total_usb()                            
                                windows_actualizacion.estado_puertos_usb = "Bloqueado"
                                windows_actualizacion.estato_actualizacion = resultado
                                windows_actualizacion.save()
                            except:
                                windows_actualizacion.estato_actualizacion = "No Actualizado"
                                windows_actualizacion.save()                                                                                                                  
                else:
                    FaltantesRevisionEquiposWindows.objects.filter(codigo_ip=ip_filtrada).delete()
                    faltantes_update_windows = FaltantesRevisionEquiposWindows()
                    faltantes_update_windows.codigo_ip = ip_filtrada
                    faltantes_update_windows.codigo_colaborador = ip_filtrada.colaborador_asignado                                    
                    faltantes_update_windows.save()                                                      
            except Exception as e:
                print(f"Error en verficiacion USB {e}")
                FaltantesRevisionEquiposWindows.objects.filter(codigo_ip=ip_filtrada).delete()
                faltantes_update_windows = FaltantesRevisionEquiposWindows()
                faltantes_update_windows.codigo_ip = ip_filtrada
                faltantes_update_windows.codigo_colaborador = ip_filtrada.colaborador_asignado                                    
                faltantes_update_windows.save()                                          
        return "TAREA VERIFICACION USB TERMINO"
    
    except Exception as e:
        return "ERROR FALTANTES INVENTARIO HARDWARE"                             
    
                             
@shared_task
def verificacion_usb_faltantes():
    try:
        try:
            año_actual = datetime.now().year
            mes_actual = datetime.now().month    
            lista_faltantes = get_list_or_404(FaltantesRevisionEquiposWindows.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual))
        except:
            return "NO HAY FALTANTES TAREA TERMINADA"
        for ip_faltantes in lista_faltantes:
            string_ip = ip_faltantes.codigo_ip.ip
            username = "Administrador"
            puerto = os.getenv('SSH_PORT')
            keyfile = os.getenv('SSH_KEYFILE')
            passphrase = os.getenv('SSH_PASSPHRASE')            
            SSH_instancia = SSHManager(string_ip,username,puerto,keyfile,passphrase)            
            ip_filtrada = ips.objects.get(ip=string_ip)
            windows_actualizacion = EstadoAccionesWindows.objects.get(id_ip=ip_filtrada.id)
            mes_actual = datetime.now().month
            año_actual = datetime.now().year
            try:                                
                print(f"********TRABAJANDO IP {string_ip}*********")  
                estado_puertos = SSH_instancia.estatus_puerto_usb()
                print(estado_puertos)
                if not estado_puertos == "Error al consultar":                               
                    FaltantesRevisionEquiposWindows.objects.filter(codigo_ip=ip_filtrada).delete()                    
                    estado_puertos = SSH_instancia.estatus_puerto_usb()                
                    if ip_filtrada.colaborador_asignado.cargo_colaborador.nombre_cargo in lista_acceso_total:                        
                        if estado_puertos.lower().strip() == 'disponible':
                            windows_actualizacion.estado_puertos_usb = "Acceso Total"
                            windows_actualizacion.save()
                        else:
                            print("Trantando de cambiarlo segun politica")
                            try:
                                resultado = SSH_instancia.ejecutar_desbloqueo_total_usb()                            
                                windows_actualizacion.estado_puertos_usb = "Acceso Total"
                                windows_actualizacion.estato_actualizacion = resultado
                                windows_actualizacion.save()
                            except:
                                windows_actualizacion.estato_actualizacion = "No Actualizado"
                                windows_actualizacion.save()
                    elif ip_filtrada.colaborador_asignado.cargo_colaborador.nombre_cargo in lista_solo_lectura or ip_filtrada.ip in ip_cajas:
                        if estado_puertos.lower().strip() == 'solo lectura':
                            windows_actualizacion.estado_puertos_usb = "Solo Lectura"
                            windows_actualizacion.save()
                        else:
                            print("Trantando de cambiarlo segun politica")
                            try:
                                resultado = SSH_instancia.ejecutar_cambiar_usb_solo_lectura()                            
                                windows_actualizacion.estado_puertos_usb = "Solo Lectura"
                                windows_actualizacion.estato_actualizacion = resultado
                                windows_actualizacion.save()
                            except:
                                windows_actualizacion.estato_actualizacion = "No Actualizado"
                                windows_actualizacion.save()
                    else:                                   
                        if estado_puertos.lower().strip() == 'bloqueado':
                            windows_actualizacion.estado_puertos_usb = "Bloqueado"
                            windows_actualizacion.save()
                        else:
                            print("Trantando de cambiarlo segun politica")
                            try:
                                resultado = SSH_instancia.ejecutar_bloqueo_total_usb()                            
                                windows_actualizacion.estado_puertos_usb = "Bloqueado"
                                windows_actualizacion.estato_actualizacion = resultado
                                windows_actualizacion.save()
                            except:
                                windows_actualizacion.estato_actualizacion = "No Actualizado"
                                windows_actualizacion.save()                                                                                                                  
                else:
                    FaltantesRevisionEquiposWindows.objects.filter(codigo_ip=ip_filtrada).delete()
                    faltantes_update_windows = FaltantesRevisionEquiposWindows()
                    faltantes_update_windows.codigo_ip = ip_filtrada
                    faltantes_update_windows.codigo_colaborador = ip_filtrada.colaborador_asignado                                    
                    faltantes_update_windows.save()                      
            except Exception as e:
                FaltantesRevisionEquiposWindows.objects.filter(codigo_ip=ip_filtrada).delete()
                print(f"Error en verficiacion USB {e}")
                faltantes_update_windows = FaltantesRevisionEquiposWindows()
                faltantes_update_windows.codigo_ip = ip_filtrada
                faltantes_update_windows.codigo_colaborador = ip_filtrada.colaborador_asignado                                    
                faltantes_update_windows.save()         
        return "TAREA FALTANTES INVENTARIO HARDWARE TERMINARDA"
    
    except Exception as e:
        return "ERROR FALTANTES INVENTARIO HARDWARE"       

@shared_task
def cambiar_usb_solo_lectura(ip):
    ip_filtrada = ips.objects.get(ip=ip)
    windows_actualizacion = EstadoAccionesWindows.objects.get(id_ip=ip_filtrada.id)
    try:
        username = "Administrador"
        puerto = os.getenv('SSH_PORT')
        keyfile = os.getenv('SSH_KEYFILE')
        passphrase = os.getenv('SSH_PASSPHRASE')
        SSH_instancia = SSHManager(ip,username,puerto,keyfile,passphrase)        
        try:
            print(f"Trabajando IP {ip_filtrada}")            
            resultado = SSH_instancia.ejecutar_cambiar_usb_solo_lectura()
            print(f"Resultado de Ejecucion comando: {resultado}")                
            if not resultado == 'No Actualizado':
                windows_actualizacion.estado_puertos_usb = "Solo Lectura"                                                                   
                windows_actualizacion.estato_actualizacion = resultado               
                windows_actualizacion.save()
            else:
                windows_actualizacion.estato_actualizacion = "No se Actualizo"
                windows_actualizacion.save()
        except Exception as e:
            print("Error no pudo actualizar no esta en red")
            windows_actualizacion.estato_actualizacion = "No se Actualizo"
            windows_actualizacion.save()
    except Exception as e:
        print("Error no pudo actualizar no esta en red")
        windows_actualizacion.estato_actualizacion = "No se Actualizo"
        windows_actualizacion.save()
        

@shared_task
def cambiar_usb_bloqueo_total(ip):
    ip_filtrada = ips.objects.get(ip=ip)
    windows_actualizacion = EstadoAccionesWindows.objects.get(id_ip=ip_filtrada.id)
    try:
        username = "Administrador"
        puerto = os.getenv('SSH_PORT')
        keyfile = os.getenv('SSH_KEYFILE')
        passphrase = os.getenv('SSH_PASSPHRASE')
        SSH_instancia = SSHManager(ip,username,puerto,keyfile,passphrase)        
        try:
            print(f"Trabajando IP {ip_filtrada}")
            resultado = SSH_instancia.ejecutar_bloqueo_total_usb()            
            if not resultado == 'No Actualizado':
                windows_actualizacion.estado_puertos_usb = "Bloqueado"                                                               
                windows_actualizacion.estato_actualizacion = resultado                
                windows_actualizacion.save()
            else:
                windows_actualizacion.estato_actualizacion = "No se Actualizo"
                windows_actualizacion.save()
        except Exception as e:
            print("Error no pudo actualizar no esta en red")
            windows_actualizacion.estato_actualizacion = "No se Actualizo"
            windows_actualizacion.save()
    except Exception as e:
        print("Error no pudo actualizar no esta en red")
        windows_actualizacion.estato_actualizacion = "No se Actualizo"
        windows_actualizacion.save()
        


@shared_task
def cambiar_usb_desbloqueo_total(ip):
    ip_filtrada = ips.objects.get(ip=ip)
    windows_actualizacion = EstadoAccionesWindows.objects.get(id_ip=ip_filtrada.id)
    try:
        username = "Administrador"
        puerto = os.getenv('SSH_PORT')
        keyfile = os.getenv('SSH_KEYFILE')
        passphrase = os.getenv('SSH_PASSPHRASE')
        SSH_instancia = SSHManager(ip,username,puerto,keyfile,passphrase)        
        try:
            print(f"Trabajando IP {ip_filtrada}")
            resultado = SSH_instancia.ejecutar_desbloqueo_total_usb() 
            if not resultado == 'No Actualizado':                 
                windows_actualizacion.estado_puertos_usb = "Acceso Total"                                                                    
                windows_actualizacion.estato_actualizacion = resultado                
                windows_actualizacion.save()
            else:
                windows_actualizacion.estato_actualizacion = "No se Actualizo"
                windows_actualizacion.save()
        except Exception as e:
            print("Error no pudo actualizar no esta en red")
            windows_actualizacion.estato_actualizacion = "No se Actualizo"
            windows_actualizacion.save()
    except Exception as e:
        print("Error no pudo actualizar no esta en red")
        windows_actualizacion.estato_actualizacion = "No se Actualizo"
        windows_actualizacion.save()


@shared_task
def hacer_reset_contraseña_windows(ip):
    ip_filtrada = ips.objects.get(ip=ip)
    windows_actualizacion = EstadoAccionesWindows.objects.get(id_ip=ip_filtrada.id)
    try:
        username = "Administrador"
        puerto = os.getenv('SSH_PORT')
        keyfile = os.getenv('SSH_KEYFILE')
        passphrase = os.getenv('SSH_PASSPHRASE')
        SSH_instancia = SSHManager(ip,username,puerto,keyfile,passphrase)        
        try:
            print(f"Trabajando IP {ip_filtrada}")            
            resultado = SSH_instancia.hacer_reset_contraseña_windows()                
            if not resultado == 'No Actualizado':                                                 
                windows_actualizacion.estato_actualizacion = resultado                
                windows_actualizacion.save()
            else:
                windows_actualizacion.estato_actualizacion = "No se Actualizo"
                windows_actualizacion.save()
        except Exception as e:
            print(f"Error no pudo actualizar no esta en red {e}")
            windows_actualizacion.estato_actualizacion = "No se Actualizo"
            windows_actualizacion.save()
    except Exception as e:
        print(f"Error no pudo actualizar no esta en red {e}")
        windows_actualizacion.estato_actualizacion = "No se Actualizo"
        windows_actualizacion.save()