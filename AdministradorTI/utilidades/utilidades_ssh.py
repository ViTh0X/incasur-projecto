import paramiko
import stat
import os
from pathlib import Path
from paramiko import SFTPError
from .utilidades_log import *
import time

class SSHManager(logArchivos):
    
    def __init__(self,hostname:str,username:str,port:int,keyfile:str,passphrase:str):        
        self.hostname = hostname
        self.username = username
        self.port = port
        self.keyfile = keyfile
        self.passphrase = passphrase
        self.conexionSSH = None
        self.canalSFTP = None
        self.rutaArchivo = None
        self.archivos_bloqueados_path_local = []
        self.archivos_bloqueados_path_remoto = []
        self.archivos_bloqueados_nombre = []
        self.archivos_bloqueados_peso = []
        self.peso_archivo_final = 0
        self.nombre_archivo_log = ""                                             

    def revisarConexionSSH(self):
        try:
            self.conexionSSH = paramiko.SSHClient()
            self.conexionSSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.conexionSSH.connect(hostname=self.hostname,port=self.port,timeout=5,username=self.username,key_filename=self.keyfile,passphrase=self.passphrase)            
            return True 
        except Exception as e:            
            print(f"No Se conecto Error : {self.hostname} - {e}")
            return False
        finally:
            if self.conexionSSH:
                self.conexionSSH.close()
                
                
    def actualizar_ejecutable_hardware(self):                
        try:
            with paramiko.SSHClient() as conexionSSH:
                self.conexionSSH = conexionSSH
                self.conexionSSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.conexionSSH.connect(hostname=self.hostname,port=self.port,timeout=15,username=self.username,key_filename=self.keyfile,passphrase=self.passphrase)                                                
                transporte = self.conexionSSH.get_transport()
                transporte.set_keepalive(20)                                                           
                ruta_archivo_origen_servidor = "/home/deployer/inventario_hardware.exe" 
                ruta_archivo_destino_cliente = "C:/Users/Administrador/Documents/TI/hardware/inventario_hardware.exe"                
                try:            
                    self.canalSFTP = self.conexionSSH.open_sftp()            
                    print("El canal SFTP creado con exito")                   
                    self.canalSFTP.put(ruta_archivo_origen_servidor,ruta_archivo_destino_cliente)                                                                                              
                    print("Copiado con exito")
                except paramiko.SFTPError as sftpE:
                    print(f"error sftp  {sftpE}")
                except Exception as e:
                    print(f"Ubo un error no creo el canal sftp{e}")
                    self.canalSFTP.close()
                    self.conexionSSH.close()                        
        except Exception as e:
            print(f"{self.hostname} Error General {e}") 
              
                    
    def actualizar_ejecutable_software(self):                
        try:
            with paramiko.SSHClient() as conexionSSH:
                self.conexionSSH = conexionSSH
                self.conexionSSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.conexionSSH.connect(hostname=self.hostname,port=self.port,timeout=15,username=self.username,key_filename=self.keyfile,passphrase=self.passphrase)                                                
                transporte = self.conexionSSH.get_transport()
                transporte.set_keepalive(20)                                          
                ruta_archivo_origen_servidor = "/home/deployer/inventario_software.exe" 
                ruta_archivo_destino_cliente = "C:/Users/Administrador/Documents/TI/software/inventario_software.exe"                
                try:            
                    self.canalSFTP = self.conexionSSH.open_sftp()            
                    print("El canal SFTP creado con exito")                   
                    self.canalSFTP.put(ruta_archivo_origen_servidor,ruta_archivo_destino_cliente)                                        
                    print("Copiado con exito")
                except paramiko.SFTPError as sftpE:
                    print(f"error sftp  {sftpE}")
                except Exception as e:
                    print(f"Ubo un error no creo el canal sftp{e}")
                    self.canalSFTP.close()
                    self.conexionSSH.close()                                    
        except Exception as e:            
            print(f"{self.hostname} Error General {e}")                           
            
    def estatus_puerto_usb(self):            
        try:
             with paramiko.SSHClient() as conexionSSH:
                self.conexionSSH = conexionSSH
                self.conexionSSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.conexionSSH.connect(hostname=self.hostname,port=self.port,timeout=15,username=self.username,key_filename=self.keyfile,passphrase=self.passphrase)                                
                transporte = self.conexionSSH.get_transport()
                transporte.set_keepalive(20)                
                script_ps = (
                    "$p = 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\RemovableStorageDevices\\{53f5630d-b6bf-11d0-94f2-00a0c91efb8b}';"
                    "$dr = 0; $dw = 0;"
                    "if (Test-Path $p) {"
                    "  $dr = (Get-ItemProperty $p).Deny_Read;"
                    "  $dw = (Get-ItemProperty $p).Deny_Write;"
                    "};"
                    "if ($dr -eq 1) { 'Bloqueado' } elseif ($dw -eq 1) { 'Solo Lectura' } else { 'Disponible' }"
                )
                comando = f"powershell.exe -NoProfile -ExecutionPolicy Bypass -Command \"& {{ {script_ps} }}\""
                stdin, stdout, stderr = conexionSSH.exec_command(comando,timeout=60)
                resultado = stdout.read().decode('cp1252', errors='replace').strip()
                
                # Si el resultado contiene varias líneas, tomamos la última que es la respuesta
                if resultado:
                    resultado = resultado.split('\n')[-1].strip()
                    
                return resultado if resultado in ['Bloqueado', 'Solo Lectura', 'Disponible'] else "Error al consultar"                                    
        except Exception as e:
            print(f"Error Capturado {e}")
            return "Error al consultar"
        

    def ejecutar_cambiar_usb_solo_lectura(self):
        try:
            with paramiko.SSHClient() as conexionSSH:
                self.conexionSSH = conexionSSH
                self.conexionSSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.conexionSSH.connect(hostname=self.hostname, port=self.port, timeout=15, username=self.username, key_filename=self.keyfile, passphrase=self.passphrase)
                
                transporte = self.conexionSSH.get_transport()
                transporte.set_keepalive(20)
                
                # Usamos comillas triples para que el script sea más legible y evitar errores de escape
                # Nota: No uses variables de Python dentro de las llaves de la política
                script_ps = (
                    "try {"
                    # 1. Definimos la ruta de la política (sin HKLM: porque el comando ya sabe que es equipo)
                    "$key = 'Software\\Policies\\Microsoft\\Windows\\RemovableStorageDevices\\{53f5630d-b6bf-11d0-94f2-00a0c91efb8b}';"
                    
                    # 2. Aplicamos 'Denegar Escritura' = 1 (Habilitado)
                    "Set-GPRegistryValue -Name 'Local Group Policy' -Key $key -ValueName 'Deny_Write' -Type DWord -Value 1 | Out-Null;"
                    
                    # 3. Aplicamos 'Denegar Lectura' = 0 (Deshabilitado para que se vea el USB)
                    "Set-GPRegistryValue -Name 'Local Group Policy' -Key $key -ValueName 'Deny_Read' -Type DWord -Value 0 | Out-Null;"
                    
                    # 4. Forzar la actualización inmediata
                    "& gpupdate /force | Out-Null;"
                    "Write-Output 'EXITO_POLITICA_REAL_APLICADA';"
                    "} catch {"
                    # Si el comando anterior no existe (versiones viejas), usamos el método REG ADD agresivo
                    "  & reg add \"HKLM\\$key\" /v Deny_Write /t REG_DWORD /d 1 /f | Out-Null;"
                    "  & reg add \"HKLM\\$key\" /v Deny_Read /t REG_DWORD /d 0 /f | Out-Null;"
                    "  & gpupdate /force | Out-Null;"
                    "  Write-Output 'EXITO_VIA_REGISTRO_DIRECTO';"
                    "}"
                )
                # IMPORTANTE: Asegúrate de que las llaves externas {{ }} rodeen al script_ps correctamente
                comando = f"powershell.exe -NoProfile -ExecutionPolicy Bypass -Command \"& {{ {script_ps} }}\""
                
                stdin, stdout, stderr = conexionSSH.exec_command(comando,timeout=60)
                
                out = stdout.read().decode('cp1252', errors='replace').strip()
                error = stderr.read().decode('cp1252', errors='replace').strip()
                
                print(f"Salida: {out}")
                
                if "EXITO_POLITICA_APLICADA" in out:
                    return "Actualizado"
                else:
                    if error:
                        print(f"Error SSH detectado: {error}")
                    return "No Actualizado"
                    
        except Exception as e:
            print(f"Error en la ejecución: {e}")
            return "No Actualizado"
                
                
    def ejecutar_bloqueo_total_usb(self):
        try:
             with paramiko.SSHClient() as conexionSSH:
                self.conexionSSH = conexionSSH
                self.conexionSSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.conexionSSH.connect(hostname=self.hostname,port=self.port,timeout=15,username=self.username,key_filename=self.keyfile,passphrase=self.passphrase)                                
                transporte = self.conexionSSH.get_transport()
                transporte.set_keepalive(20)                
                script_ps = (
                    "try {"
                    "$key = 'Software\\Policies\\Microsoft\\Windows\\RemovableStorageDevices\\{53f5630d-b6bf-11d0-94f2-00a0c91efb8b}';"
                    # Bloqueamos Lectura y Escritura
                    "Set-GPRegistryValue -Name 'Local Group Policy' -Key $key -ValueName 'Deny_Read' -Type DWord -Value 1 | Out-Null;"
                    "Set-GPRegistryValue -Name 'Local Group Policy' -Key $key -ValueName 'Deny_Write' -Type DWord -Value 1 | Out-Null;"
                    "& gpupdate /force | Out-Null;"
                    "Write-Output 'EXITO_BLOQUEO_TOTAL';"
                    "} catch {"
                    "  & reg add \"HKLM\\$key\" /v Deny_Read /t REG_DWORD /d 1 /f | Out-Null;"
                    "  & reg add \"HKLM\\$key\" /v Deny_Write /t REG_DWORD /d 1 /f | Out-Null;"
                    "  & gpupdate /force | Out-Null;"
                    "  Write-Output 'EXITO_BLOQUEO_TOTAL_REG';"
                    "}"
                )
                comando = f"powershell.exe -NoProfile -ExecutionPolicy Bypass -Command \"& {{ {script_ps} }}\""
                stdin, stdout,stderr = self.conexionSSH.exec_command(comando,timeout=60)
                out = stdout.read().decode('cp1252', errors='replace')
                return "Actualizado" if "EXITO" in out else "No Actualizado"                
        except:
            return "No Actualizado"
                

    def ejecutar_desbloqueo_total_usb(self):
        try:
             with paramiko.SSHClient() as conexionSSH:
                self.conexionSSH = conexionSSH
                self.conexionSSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.conexionSSH.connect(hostname=self.hostname,port=self.port,timeout=15,username=self.username,key_filename=self.keyfile,passphrase=self.passphrase)                                
                transporte = self.conexionSSH.get_transport()
                transporte.set_keepalive(20)                
                script_ps = (
                    "try {"
                    "$key = 'Software\\Policies\\Microsoft\\Windows\\RemovableStorageDevices\\{53f5630d-b6bf-11d0-94f2-00a0c91efb8b}';"
                    # Liberamos Lectura y Escritura
                    "Set-GPRegistryValue -Name 'Local Group Policy' -Key $key -ValueName 'Deny_Read' -Type DWord -Value 0 | Out-Null;"
                    "Set-GPRegistryValue -Name 'Local Group Policy' -Key $key -ValueName 'Deny_Write' -Type DWord -Value 0 | Out-Null;"
                    "& gpupdate /force | Out-Null;"
                    "Write-Output 'EXITO_DESBLOQUEO';"
                    "} catch {"
                    "  & reg add \"HKLM\\$key\" /v Deny_Read /t REG_DWORD /d 0 /f | Out-Null;"
                    "  & reg add \"HKLM\\$key\" /v Deny_Write /t REG_DWORD /d 0 /f | Out-Null;"
                    "  & gpupdate /force | Out-Null;"
                    "  Write-Output 'EXITO_DESBLOQUEO_REG';"
                    "}"
                )
                comando = f"powershell.exe -NoProfile -ExecutionPolicy Bypass -Command \"& {{ {script_ps} }}\""
                stdin, stdout,stderr = self.conexionSSH.exec_command(comando,timeout=60)
                out = stdout.read().decode('cp1252', errors='replace')
                return "Actualizado" if "EXITO" in out else "No Actualizado"         
        except:
            return "No Actualizado"              
    
        
    def hacer_reset_contraseña_windows(self):
        try:
            with paramiko.SSHClient() as conexionSSH:
                conexionSSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                conexionSSH.connect(
                    hostname=self.hostname,
                    port=self.port,
                    timeout=15,
                    username=self.username,
                    key_filename=self.keyfile,
                    passphrase=self.passphrase
                )
                script_ps = (
                    # 1. Obtener nombre del grupo de admins por SID (S-1-5-32-544)
                    "$adminGroupName = (Get-LocalGroup -SID 'S-1-5-32-544').Name;"
                    
                    # 2. Obtener nombres limpios de los miembros del grupo admin
                    "$admins = (Get-LocalGroupMember -Group $adminGroupName).Name | ForEach-Object { $_ -split '\\\\' | Select-Object -Last 1 };"
                    
                    # 3. FILTRO MEJORADO: 
                    # - Debe estar habilitado
                    # - NO debe estar en la lista de admins
                    # - NO debe llamarse 'Administrador' o 'Administrator'
                    # - Su SID NO debe terminar en -500 (que es la cuenta admin integrada)
                    "$usuarios = Get-LocalUser | Where-Object { "
                    "  $_.Enabled -eq $true -and "
                    "  $admins -notcontains $_.Name -and "
                    "  $_.Name -notmatch 'Administrador|Administrator' -and "
                    "  $_.SID.Value -notmatch '-500$'"
                    "};"
                    
                    "foreach ($u in $usuarios) {"
                    "  try {"
                    "    $username = $u.Name;"
                    "    & net user \"$username\" 2026_informacion /y | Out-Null;"
                    "    & net user \"$username\" /logonpasswordchg:yes | Out-Null;"
                    "    Write-Output ('EXITO_CAMBIO: ' + $username);"
                    "  } catch {"
                    "    Write-Output ('ERROR_EN: ' + $u.Name);"
                    "  }"
                    "}"
                )
                comando = f"powershell.exe -NoProfile -ExecutionPolicy Bypass -Command \"& {{ {script_ps} }}\""                                
                                
                stdin, stdout, stderr = conexionSSH.exec_command(comando,timeout=60)
                
                error = stderr.read().decode('cp1252', errors='replace').strip()
                if error:
                    # Si hay error (ej. permisos insuficientes), devolvemos "No Actualizado"
                    print(error)
                    return "No Actualizado"
                
                return "Actualizado"
        except Exception as e:
            print(f"Error es {e}")
            return "No Actualizado"                 
                                        
    def ejecuta_inventario_hardware(self):                       
        try:
            with paramiko.SSHClient() as conexionSSH:
                self.conexionSSH = conexionSSH
                self.conexionSSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.conexionSSH.connect(hostname=self.hostname,port=self.port,timeout=15,username=self.username,key_filename=self.keyfile,passphrase=self.passphrase)                                
                transporte = self.conexionSSH.get_transport()
                transporte.set_keepalive(20)                
                                                      
                #time.sleep(5)                
                
                ruta_inventario_hardware = f"C:/Users/Administrador/Documents/TI/hardware/{self.hostname}-hardware.txt"
                ruta_archivo_local = f"/home/deployer/Inventarios/{self.hostname}-hardware.txt"
                #ruta_archivo_local = f"D:/Inventarios/{self.hostname}-hardware.txt"        
                ruta_archivo_origen_servidor = "/home/deployer/inventario_hardware.exe" 
                ruta_archivo_destino_cliente = "C:/Users/Administrador/Documents/TI/hardware/inventario_hardware.exe"
                try:
                    self.canalSFTP = self.conexionSSH.open_sftp()  
                    print("El canal SFTP creado con exito")                                                           
                    self.canalSFTP.put(ruta_archivo_origen_servidor,ruta_archivo_destino_cliente)
                    print("Archivo Actualizado")
                    
                    try:                                                          
                        comando = "C:/Users/Administrador/Documents/TI/hardware/inventario_hardware.exe"
                        stdin, stdout,stderr = self.conexionSSH.exec_command(comando)
                        stdout.read()
                        stderr.read() 
                        exit_status = stdout.channel.recv_exit_status()
                        print("Inventario_hardware ejecutado con exito")
                    except Exception as e:
                        print(f"Error al ejecutar el archivo no lo encontro *** {e}")   
                                                                         
                    self.canalSFTP.get(ruta_inventario_hardware,ruta_archivo_local)
                    print("Archivo inventario copiado con exito")                    
                except paramiko.SFTPError as sftpE:
                    print(f"error sftp  {sftpE}")
                except Exception as e:
                    print(f"Ubo un error no creo el canal sftp{e}")
                    self.canalSFTP.close()
                    self.conexionSSH.close() 
            return True
                               
        except Exception as e:            
            print(f"{self.hostname} Error General {e}")
            return False
        
                       
        
    def guardar_inventario_hardware(self):
        dic_inventario_hardware = {}           
        ruta_archivo_local = f"/home/deployer/Inventarios/{self.hostname}-hardware.txt"
        # ruta_archivo_local = f"D:/Inventarios/{self.hostname}-hardware.txt"                                    
        with open(ruta_archivo_local,'r',encoding='windows-1252') as inventario_hardware:
            for linea in inventario_hardware:
                if "Nombre" in linea:   #0              
                    data = linea[linea.find(":")+1:len(linea)].replace('\n','').strip()
                    nombre_pc = data
                    dic_inventario_hardware['nombre_pc'] = nombre_pc
                elif "Placa" in linea: #1                
                    data = linea[linea.find(":")+1:len(linea)].replace('\n','').strip()
                    placa = data
                    dic_inventario_hardware['placa'] = placa
                elif "Procesador" in linea:       #2          
                    data = linea[linea.find(":")+1:len(linea)].replace('\n','').strip()
                    procesador = data       
                    dic_inventario_hardware['procesador'] = procesador                  
                elif "Ram" in linea:       #3          
                    data = linea[linea.find(":")+1:len(linea)].replace('\n','').strip()
                    ram = data
                    dic_inventario_hardware['ram'] = ram     
                elif "Tarjeta Integrada" in linea:       #4          
                    data = linea[linea.find(":")+1:len(linea)].replace('\n','').strip()
                    tarjeta_integrada = data          
                    dic_inventario_hardware['tarjeta_integrada'] = tarjeta_integrada                   
                elif "Tarjeta Dedicada" in linea:       #5          
                    data = linea[linea.find(":")+1:len(linea)].replace('\n','').strip()
                    tarjeta_dedicada = data      
                    dic_inventario_hardware['tarjeta_dedicada'] = tarjeta_dedicada
                elif "S.O." in linea: #6                
                    data = linea[linea.find(":")+1:len(linea)].replace('\n','').strip()                    
                    sistema_operativo = data      
                    dic_inventario_hardware['sistema_operativo'] = sistema_operativo    
                elif "Puerta Enlace" in linea:    #7             
                    data = linea[linea.find(":")+1:len(linea)].replace('\n','').strip()
                    puerta_enlace = data     
                    dic_inventario_hardware['puerta_enlace'] = puerta_enlace                                         
                elif "Almacenamiento" in linea:    #7             
                    data = linea[linea.find(":")+1:len(linea)].replace('\n','').strip()
                    almacenamiento = data     
                    dic_inventario_hardware['almacenamiento'] = almacenamiento
        return dic_inventario_hardware
    
    
    def ejecuta_inventario_software(self):                       
        try:            
            with paramiko.SSHClient() as conexionSSH:
                self.conexionSSH = conexionSSH
                self.conexionSSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.conexionSSH.connect(hostname=self.hostname,port=self.port,timeout=15,username=self.username,key_filename=self.keyfile,passphrase=self.passphrase)            
                transporte = self.conexionSSH.get_transport()
                transporte.set_keepalive(20)                                
                
                #time.sleep(10)
                ruta_inventario_hardware = f"C:/Users/Administrador/Documents/TI/software/{self.hostname}-software.txt"
                ruta_archivo_local = f"/home/deployer/Inventarios/{self.hostname}-software.txt"
                # ruta_archivo_local = f"D:/Inventarios/{self.hostname}-software.txt"
                ruta_archivo_origen_servidor = "/home/deployer/inventario_software.exe" 
                ruta_archivo_destino_cliente = "C:/Users/Administrador/Documents/TI/software/inventario_software.exe"                
                try:                                
                    self.canalSFTP = self.conexionSSH.open_sftp()
                    print("Canala SFTP Creado")  
                    self.canalSFTP.put(ruta_archivo_origen_servidor,ruta_archivo_destino_cliente)                                    
                    print("Ejecutable Actualizado")
                    try:                                                                
                        comando = "C:/Users/Administrador/Documents/TI/software/inventario_software.exe"
                        stdin, stdout,stderr = self.conexionSSH.exec_command(comando)
                        stdout.read()
                        stderr.read()
                        exit_status = stdout.channel.recv_exit_status()                 
                        print("Inventario_software ejecutado con exito")                    
                    except Exception as e:
                        print(f"Error al ejecutar el archivo no lo encontro **** {e}")
                    self.canalSFTP.get(ruta_inventario_hardware,ruta_archivo_local)
                    print("Archivo inventario software guardado")
                except paramiko.SFTPError as sftpE:
                    print(f"error sftp  {sftpE}")
                except Exception as e:
                    print(f"Ubo un error no creo el canal sftp{e}")
                    self.canalSFTP.close()
                    self.conexionSSH.close()
            return True 
        except Exception as e:
            print(f"{self.hostname} Error general {e}")                            
            return False
        
                       
        
    def guardar_inventario_software(self):
        try:
            lista_office=[]
            lista_acceso_remoto=[]
            lista_editores_texto=[]
            lista_base_datos=[]
            lista_pdf=[]
            lista_ftia=[]
            lista_impresoras=[]
            lista_navegadores=[]
            lista_compresores=[]
            lista_drivers=[]
            lista_drive=[]
            lista_TI=[]
            lista_otros=[]                  
            ruta_archivo_local = f"/home/deployer/Inventarios/{self.hostname}-software.txt"
            # ruta_archivo_local = f"D:/Inventarios/{self.hostname}-software.txt"                                            
            with open(ruta_archivo_local,'r') as inventario_software:
                for linea in inventario_software:
                    if "Office" in linea:   #0              
                        data = linea[linea.find(":")+1:len(linea)].replace('\n','').strip()
                        lista_office.append(data)
                    elif "Acceso Remoto" in linea: #1                
                        data = linea[linea.find(":")+1:len(linea)].replace('\n','').strip()
                        lista_acceso_remoto.append(data)                    
                    elif "Editores Texto" in linea:       #2          
                        data = linea[linea.find(":")+1:len(linea)].replace('\n','').strip()
                        lista_editores_texto.append(data)
                    elif "Base Datos" in linea:       #3          
                        data = linea[linea.find(":")+1:len(linea)].replace('\n','').strip()
                        lista_base_datos.append(data)
                    elif "PDF" in linea:       #4          
                        data = linea[linea.find(":")+1:len(linea)].replace('\n','').strip()
                        lista_pdf.append(data)
                    elif "FTIA" in linea:       #5          
                        data = linea[linea.find(":")+1:len(linea)].replace('\n','').strip()
                        lista_ftia.append(data)                    
                    elif "Impresoras" in linea: #6                
                        data = linea[linea.find(":")+1:len(linea)].replace('\n','').strip()                    
                        lista_impresoras.append(data)
                    elif "Navegadores" in linea:    #7             
                        data = linea[linea.find(":")+1:len(linea)].replace('\n','').strip()
                        lista_navegadores.append(data)
                    elif "Compresores" in linea:    #7             
                        data = linea[linea.find(":")+1:len(linea)].replace('\n','').strip()
                        lista_compresores.append(data)
                    elif "Drivers" in linea:
                        data = linea[linea.find(":")+1:len(linea)].replace('\n','').strip()
                        lista_drivers.append(data)
                    elif "Drivers" in linea:
                        data = linea[linea.find(":")+1:len(linea)].replace('\n','').strip()
                        lista_drivers.append(data)
                    elif "Drive" in linea:
                        data = linea[linea.find(":")+1:len(linea)].replace('\n','').strip()
                        lista_drive.append(data)
                    elif "T. I." in linea:
                        data = linea[linea.find(":")+1:len(linea)].replace('\n','').strip()
                        lista_TI.append(data)
                    elif "Otros" in linea:
                        data = linea[linea.find(":")+1:len(linea)].replace('\n','').strip()
                        lista_otros.append(data)
                dic_inventario_software = {
                    1:lista_office,
                    2:lista_acceso_remoto,
                    3:lista_editores_texto,
                    4:lista_base_datos,
                    5:lista_pdf,
                    6:lista_ftia,
                    7:lista_impresoras,
                    8:lista_navegadores,
                    9:lista_compresores,
                    10:lista_drivers,
                    11:lista_drive,
                    12:lista_TI,
                    13:lista_otros                
                }                     
            return dic_inventario_software
        except Exception as e:
            print(f"Error leyendo archivo {e}")
        
    def realizarConSSH(self):
        self.rutaArchivo = self.crearArchivo(self.hostname)
        dd = datetime.now().day
        mm =  datetime.now().month
        yyyy = datetime.now().year  
        self.nombre_archivo_log = f"Log-{self.hostname}--{yyyy}-{mm}-{dd}"
        try:                        
            self.conexionSSH = paramiko.SSHClient()            
            self.conexionSSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())            
            mensaje = f"Intentando Realizar conexion a {self.hostname} con el usuario {self.username}."
            self.registrarLog(mensaje,"INF",self.rutaArchivo,self.hostname)
            self.conexionSSH.connect(hostname=self.hostname,port=self.port,timeout=15,banner_timeout=30,username=self.username,key_filename=self.keyfile,passphrase=self.passphrase)                                                
            transport = self.conexionSSH.get_transport()
            if transport:
                transport.set_keepalive(30)
            return True
        except paramiko.SSHException as e:
            self.registrarLog(f"Error de protocolo SSH: {e}","ERR",self.rutaArchivo,self.hostname) 
            if self.conexionSSH:
                self.conexionSSH.close()
            return False
        except paramiko.AuthenticationException as sshE:            
            mensaje = f"Error al establecer conexion SSH a host {self.hostname} al usuario {self.username}"
            self.registrarLog(mensaje,"ERR",self.rutaArchivo,self.hostname)
            if self.conexionSSH:
                self.conexionSSH.close()
            return False
        except Exception as e:
            mensaje = f"Ocurrio un error inesperado : {e}"
            self.registrarLog(mensaje,"ERR",self.rutaArchivo,self.hostname)
            if self.conexionSSH:
                self.conexionSSH.close()
            return False
        # finally:
        #     if self.conexionSSH:
        #         self.conexionSSH.close()        
    
    
    def crearCanalSFTP(self):
        try:
            self.canalSFTP = self.conexionSSH.open_sftp()
            mensaje = f"Se creo canal SFTP para {self.hostname} de manera exitosa"            
            self.registrarLog(mensaje,"INF",self.rutaArchivo,self.hostname)            
        except paramiko.SFTPError as sftpE:
            mensaje = f"Error al crear canal SFTP {sftpE} para {self.hostname}"
            self.registrarLog(mensaje,"ERR",self.rutaArchivo,self.hostname)            
    
    
    def rutasIniciales(self,listaCarpetas:list):
        try:
            rutaBase = Path("/mnt/backupinformacion/colaboradores_data")
            #rutaInicial = f"/mnt/backupcolaboradores/{self.hostname}/"
            rutaInicial = rutaBase / self.hostname
            print(f"Ruta inicial creada {rutaInicial} --- {self.hostname}")
        except Exception as e:
            print(f"Error creando ruta {e}")
        listaRutasLocales = []                
        os.makedirs(rutaInicial,exist_ok=True)
        for carpetas in listaCarpetas:
            print(f"Creando{carpetas}")
            ruta = Path(rutaInicial)/carpetas
            os.makedirs(ruta,exist_ok=True)
            print(f"Esto se creo {ruta}")        
            listaRutasLocales.append(ruta)
            mensaje = "Las carpetas iniciales en el Disco /mnt/backupinformacion/colaboradores_data fueron creadas con exito"
            self.registrarLog(mensaje,"INF",self.rutaArchivo,self.hostname)
        return listaRutasLocales
    
    
    def creaRutasRemotas(self,usuario:str,listaRutaLocales:list,ip:str):        
        lsRutaBKUP = []
        rBaseRemoC = "C:/Users/"        
        try:
            '''if ip == "192.168.1.30":
                for rLocal in listaRutaLocales:
                    lsR = {}
                    rutaTexto = str(rLocal)
                    if "Discos" in rutaTexto:                                                                            
                        ruta ="D:\JSALASBACKUP"
                        local = Path(rLocal)/"Disco_D"
                        os.makedirs(local,exist_ok=True)
                        lsR[local] = ruta
                        lsRutaBKUP.append(lsR)
                        lsR = {}
                mensaje = "Las rutas iniciales fueron preparadas con exito"
                self.registrarLog(mensaje,"INF",self.rutaArchivo,self.hostname)
                return lsRutaBKUP   '''         
            if ip == "192.168.1.36":
                for rLocal in listaRutaLocales:
                    lsR = {}
                    rutaTexto = str(rLocal)
                    if "Discos" in rutaTexto:                                                                            
                        ruta ="C:\Patrick"
                        local = Path(rLocal)/"Disco_D"
                        os.makedirs(local,exist_ok=True)
                        lsR[local] = ruta
                        lsRutaBKUP.append(lsR)
                        lsR = {}
                mensaje = "Las rutas iniciales fueron preparadas con exito"
                self.registrarLog(mensaje,"INF",self.rutaArchivo,self.hostname)
                return lsRutaBKUP
            else:
                for rLocal in listaRutaLocales:            
                    lsR = {}
                    rutaTexto = str(rLocal)
                    if "Documentos" in rutaTexto:                    
                        ruta = Path(rBaseRemoC)/usuario/"Documents"                    
                        lsR[rLocal] = ruta
                        lsRutaBKUP.append(lsR)                    
                    elif "Descargas" in rutaTexto:                    
                        ruta = Path(rBaseRemoC)/usuario/"Downloads"
                        lsR[rLocal] = ruta
                        lsRutaBKUP.append(lsR)                    
                    elif "Escritorio" in rutaTexto:                    
                        ruta = Path(rBaseRemoC)/usuario/"Desktop"
                        lsR[rLocal] = ruta
                        lsRutaBKUP.append(lsR)                    
                    elif "Discos" in rutaTexto:                    
                        ruta = "D:/"
                        local = Path(rLocal)/"Disco_D"
                        os.makedirs(local,exist_ok=True)        
                        lsR[local] = ruta
                        lsRutaBKUP.append(lsR)
                        lsR = {}
                        '''
                        ruta ="E:/"
                        local = Path(rLocal)/"Disco_E"
                        lsR[local] = ruta
                        lsRutaBKUP.append(lsR)
                        lsR = {}
                        ruta ="F:/"
                        local = Path(rLocal)/"Disco_F"
                        lsR[local] = ruta
                        lsRutaBKUP.append(lsR)
                        lsR = {}
                        ruta ="G:/"
                        local = Path(rLocal)/"Disco_G"
                        lsR[local] = ruta
                        lsRutaBKUP.append(lsR)
                        lsR = {}
                        ruta ="H:/"
                        local = Path(rLocal)/"Disco_H"
                        lsR[local] = ruta
                        lsRutaBKUP.append(lsR)
                        lsR = {}   '''                 
                mensaje = "Las rutas iniciales fueron preparadas con exito"
                self.registrarLog(mensaje,"INF",self.rutaArchivo,self.hostname)
                return lsRutaBKUP
        except Exception as e:
            mensaje = f"Error preparando las rutas : {e}"
            self.registrarLog(mensaje,"ERR",self.rutaArchivo,self.hostname)


    def copiar_pst(self):
        print("Funcion copiar_pst Ejecutada")
        print(f"Lista archivos ocupados1: {self.archivos_bloqueados_path_local}")
        print(f"Lista archivos ocupados2: {self.archivos_bloqueados_path_remoto}")
        print(f"Lista nombre archivos: {self.archivos_bloqueados_nombre}")
        if len(self.archivos_bloqueados_nombre) > 0:
            ubicacion = 0
            for ruta_retoma in self.archivos_bloqueados_path_remoto:                        
                try:
                    mensaje = f"Copiando archivo {self.archivos_bloqueados_nombre[ubicacion]}"
                    self.registrarLog(mensaje,"INF",ruta_retoma,self.hostname) 
                    print("Intentando copiar el PST")                        
                    mensaje = f"De {ruta_retoma} --> {self.archivos_bloqueados_path_local[ubicacion]}"
                    self.registrarLog(mensaje,"INF",ruta_retoma,self.hostname)  
                    self.canalSFTP.get(str(ruta_retoma),str(self.archivos_bloqueados_path_local[ubicacion]))
                    mensaje = f"Archivo {self.archivos_bloqueados_nombre[ubicacion]} salvado con EXITO"
                    self.registrarLog(mensaje,"INF",ruta_retoma,self.hostname)
                    self.peso_archivo_final += self.archivos_bloqueados_peso[ubicacion]  
                except IOError as e:
                    mensaje = f"No se pudo copiar {self.archivos_bloqueados_nombre[ubicacion]} (¿Archivo en uso?): {e}"
                    self.registrarLog(mensaje, "ERR",ruta_retoma, self.hostname)                    
                ubicacion += 1
        else:
            print("No se encontro ningun pst")                
            
    def comprobar_extesiones_permitidas(self,nombre_archivo):
        lista_extensiones = ['.xls','.xlsx','.csv','.doc','.docx','.csv','.ppt','.pptx']
        for extension in lista_extensiones:
            if extension in str(nombre_archivo):
                return True
        return False
            
    def realizarBKUP(self,rBaseRemo:str,rBaseLocal:str,nombreCarpeta:str):                                        
        # --- VALIDACIÓN CRÍTICA ---
        transport = self.conexionSSH.get_transport() if self.conexionSSH else None
        if self.conexionSSH is None or transport is None or not transport.is_active():
            self.registrarLog("CONEXIÓN CERRADA: Abortando rama de backup.", "ERR", self.rutaArchivo, self.hostname)
            return
        if nombreCarpeta != "":
            baseR = Path(rBaseRemo)
            rBaseRemoR = baseR / nombreCarpeta
            baseL = Path(rBaseLocal)
            rBaseLocalR = baseL / nombreCarpeta
        else:            
            rBaseRemoR = Path(rBaseRemo)
            rBaseLocalR = Path(rBaseLocal)
        try:                
            listaArchivos = list(self.canalSFTP.listdir_iter(str(rBaseRemoR)))                                             
            for archivo in listaArchivos:                                                                   
                nombreArchivo = archivo.filename                                                
                if nombreArchivo.startswith("~"):
                    print(f"Archivo {nombreArchivo} ignorado")
                    continue                
                else:                    
                    if stat.S_ISDIR(archivo.st_mode):
                        if nombreArchivo == "System Volume Information" or nombreArchivo == "$RECYCLE.BIN":
                            print(f"Ignorando Carpeta System Volume Information, RECYCLE,Plantillas y su contenido")
                            continue                        
                        creaRutaLocal = rBaseLocalR / nombreArchivo
                        try:
                            os.makedirs(creaRutaLocal,exist_ok=True)
                        except Exception as e:
                            print(f"Error en la carpeta {nombreArchivo} - {e}")
                        mensaje = f"Se creo la carpeta {nombreArchivo} - Ruta {creaRutaLocal}"
                        self.registrarLog(mensaje,"INF",self.rutaArchivo,self.hostname)                                                            
                        self.realizarBKUP(rBaseRemoR,rBaseLocalR,nombreArchivo)                                            
                    else:                
                        peso_archivo = archivo.st_size
                        peso_final = peso_archivo / (1024 * 1024)
                        es_archivo_office = self.comprobar_extesiones_permitidas(nombreArchivo)                                                                                                                                                                                                                                                                                                                                                   
                        rutaCopiarLocal = rBaseLocalR / nombreArchivo                          
                        rutaCopiarRemoto = rBaseRemoR / nombreArchivo 
                        existeLocal = os.path.exists(str(rutaCopiarLocal))                        
                        try:                            
                            if not existeLocal:                                                                
                                mensaje = f"Copiando archivo {nombreArchivo}"
                                self.registrarLog(mensaje,"INF",self.rutaArchivo,self.hostname)             
                                mensaje = f"De {rutaCopiarRemoto} --> {rutaCopiarLocal}"
                                self.registrarLog(mensaje,"INF",self.rutaArchivo,self.hostname)  
                                try:
                                    if not es_archivo_office:        
                                        with self.canalSFTP.open(str(rutaCopiarRemoto),'r+') as prueba_abrir:
                                            pass                                                                                                                  
                                    self.canalSFTP.get(str(rutaCopiarRemoto),str(rutaCopiarLocal))                                    
                                    mensaje = f"Archivo {nombreArchivo} salvado con EXITO"
                                    self.registrarLog(mensaje,"INF",self.rutaArchivo,self.hostname)
                                    self.peso_archivo_final += int(peso_final)
                                except IOError as e:
                                    self.archivos_bloqueados_path_local.append(rutaCopiarLocal)
                                    self.archivos_bloqueados_path_remoto.append(rutaCopiarRemoto)
                                    self.archivos_bloqueados_nombre.append(nombreArchivo)
                                    print(f"Lista archivos ocupados1: {self.archivos_bloqueados_path_local}")
                                    print(f"Lista archivos ocupados2: {self.archivos_bloqueados_path_remoto}")
                                    print(f"Lista nombre archivos: {self.archivos_bloqueados_nombre}")
                                    mensaje = f"No se pudo copiar {nombreArchivo} (¿Archivo en uso?): {e}"
                                    self.registrarLog(mensaje, "ERR", self.rutaArchivo, self.hostname)
                                    self.archivos_bloqueados_peso.append(int(peso_final))                                              
                                except Exception as e:
                                    print(f"No copio el archivo {e} - {rutaCopiarRemoto}")
                                    if "Socket is closed" in str(e):
                                        self.cerrarConexiones()                                             
                            else:    
                                tamañoRemoto = archivo.st_size
                                tamañoLocal = os.path.getsize(rutaCopiarLocal)                            
                                if tamañoRemoto != tamañoLocal:
                                    mensaje = f"Copiando archivo {nombreArchivo}"
                                    self.registrarLog(mensaje,"INF",self.rutaArchivo,self.hostname)             
                                    mensaje = f"De {rutaCopiarRemoto} --> {rutaCopiarLocal}"
                                    self.registrarLog(mensaje,"INF",self.rutaArchivo,self.hostname)                                                                                                              
                                    try:
                                        if not es_archivo_office:        
                                            with self.canalSFTP.open(str(rutaCopiarRemoto),'r+') as prueba_abrir:
                                                pass                                                                                                                           
                                        self.canalSFTP.get(str(rutaCopiarRemoto),str(rutaCopiarLocal))
                                        mensaje = f"Archivo {nombreArchivo} salvado con EXITO"
                                        self.registrarLog(mensaje,"INF",self.rutaArchivo,self.hostname)
                                        self.peso_archivo_final += int(peso_final)
                                    except IOError as e:
                                        self.archivos_bloqueados_path_local.append(rutaCopiarLocal)
                                        self.archivos_bloqueados_path_remoto.append(rutaCopiarRemoto)
                                        self.archivos_bloqueados_nombre.append(nombreArchivo)
                                        print(f"Lista archivos ocupados1: {self.archivos_bloqueados_path_local}")
                                        print(f"Lista archivos ocupados2: {self.archivos_bloqueados_path_remoto}")
                                        print(f"Lista nombre archivos: {self.archivos_bloqueados_nombre}")
                                        mensaje = f"No se pudo copiar {nombreArchivo} (¿Archivo en uso?): {e}"
                                        self.registrarLog(mensaje, "ERR", self.rutaArchivo, self.hostname)
                                        self.archivos_bloqueados_peso.append(int(peso_final))                                        
                                    except Exception as e:
                                        print(f"No copio el archivo {e} - {rutaCopiarRemoto}")
                                        if "Socket is closed" in str(e):
                                            self.cerrarConexiones()                                                                     
                                else:                                    
                                    mensaje = f"El archivo {nombreArchivo} ya fue guardado de manera local"
                                    self.registrarLog(mensaje,"INF",self.rutaArchivo,self.hostname)        
                                    self.peso_archivo_final += int(peso_final)     
                        except FileNotFoundError as e:                        
                            print(f"Error posiblemente el archivo no existe : {e} - {rutaCopiarRemoto}")
                            mensaje = f"Error posiblemente el archivo no existe : {e} - {rutaCopiarRemoto}"
                            self.registrarLog(mensaje,"ERR",self.rutaArchivo,self.hostname)                        
                        except Exception as e:                        
                            print(f"Ocurrio un error inesperado : {e} bucle 1 - {rutaCopiarRemoto}")
                            mensaje = f"Ocurrio un error inesperado : {e} -{rutaCopiarRemoto}"
                            self.registrarLog(mensaje,"ERR",self.rutaArchivo,self.hostname)                                                                                                                                                       
        except SFTPError as e:            
            print(f"Error en la carpeta {rBaseRemoR} posiblemente no existe : {e}")
            mensaje = f"Error en la carpeta {rBaseRemoR} posiblemente no existe : {e}"
            self.registrarLog(mensaje,"ERR",self.rutaArchivo,self.hostname)            
        except FileExistsError as e:            
            print(f"Error en ruta {rBaseRemoR} posiblemente no existe : {e}")
            mensaje = f"Error en ruta {rBaseRemoR} posiblemente no existe : {e}"
            self.registrarLog(mensaje,"ERR",self.rutaArchivo,self.hostname)                                          
        except Exception as e:                                    
            print(f"Ocurrio un error inesperado {e} - {rBaseRemoR} - {rBaseLocalR}")            
            mensaje = f"Ocurrio un error inesperado {e} - {rBaseRemoR} - {rBaseLocalR}"
            self.registrarLog(mensaje,"ERR",self.rutaArchivo,self.hostname)                   
                
    def cerrarConexiones(self):
        self.canalSFTP.close()
        self.conexionSSH.close()