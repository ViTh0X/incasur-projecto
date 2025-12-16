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

    def revisarConexionSSH(self):
        try:
            self.conexionSSH = paramiko.SSHClient()
            self.conexionSSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.conexionSSH.connect(hostname=self.hostname,port=self.port,timeout=3,username=self.username,key_filename=self.keyfile,passphrase=self.passphrase)            
            return True 
        except Exception as e:            
            print(f"No Se conecto Error : {self.hostname} - {e}")
            return False
        finally:
            if self.conexionSSH:
                self.conexionSSH.close()
                
    def ejecuta_inventario_hardware(self):                       
        try:
            with paramiko.SSHClient() as conexionSSH:
                self.conexionSSH = conexionSSH
                self.conexionSSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.conexionSSH.connect(hostname=self.hostname,port=self.port,timeout=15,username=self.username,key_filename=self.keyfile,passphrase=self.passphrase)                                
                try:                  
                    comando = "C:/Users/Administrador/Documents/TI/hardware/inventario_hardware.exe"
                    stdin, stdout,stderr = self.conexionSSH.exec_command(comando)
                    stdout.read()
                    stderr.read() 
                    print("Inventario_hardware ejecutado con exito")
                except Exception as e:
                    print("Error al ejecutar el archivo no lo encontro")
                time.sleep(5)
                #ruta_archivo_origen_servidor = "/root/inventario_hardware.exe" 
                #ruta_archivo_destino_cliente = "C:/Users/Administrador/Documents/TI/hardware/inventario_hardware.exe"
                ruta_inventario_hardware = f"C:/Users/Administrador/Documents/TI/hardware/{self.hostname}-hardware.txt"
                ruta_archivo_local = f"/root/Inventarios/{self.hostname}-hardware.txt"
                #ruta_archivo_local = f"D:/Inventarios/{self.hostname}-hardware.txt"        
                try:            
                    self.canalSFTP = self.conexionSSH.open_sftp()            
                    print("El canal SFTP creado con exito")                   
                    #self.canalSFTP.put(ruta_archivo_origen_servidor,ruta_archivo_destino_cliente)
                    self.canalSFTP.get(ruta_inventario_hardware,ruta_archivo_local)
                    print("Archivo inventario copiado")
                    #print("Copiado con exito")
                except paramiko.SFTPError as sftpE:
                    print(f"error sftp  {sftpE}")
                except Exception as e:
                    print(f"Ubo un error no creo el canal sftp{e}")
                    self.canalSFTP.close()
                    self.conexionSSH.close()                        
        except Exception as e:
            print(f"Error General {e}")
        
                       
        
    def guardar_inventario_hardware(self):
        dic_inventario_hardware = {}           
        ruta_archivo_local = f"/root/Inventarios/{self.hostname}-hardware.txt"
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
                        
                comando = "C:/Users/Administrador/Documents/TI/software/inventario_software.exe"
                stdin, stdout,stderr = self.conexionSSH.exec_command(comando)
                stdout.read()
                stderr.read() 
                time.sleep(5)
                print("Inventario_software ejecutado con exito")
                ruta_inventario_hardware = f"C:/Users/Administrador/Documents/TI/software/{self.hostname}-software.txt"
                ruta_archivo_local = f"/root/Inventarios/{self.hostname}-software.txt"
                # ruta_archivo_local = f"D:/Inventarios/{self.hostname}-software.txt"
                try:
                    self.canalSFTP = self.conexionSSH.open_sftp()                   
                    self.canalSFTP.get(ruta_inventario_hardware,ruta_archivo_local)
                except paramiko.SFTPError as sftpE:
                    print(f"error sftp  {sftpE}")
                except Exception as e:
                    print(f"Ubo un error no creo el canal sftp{e}")
                    self.canalSFTP.close()
                    self.conexionSSH.close() 
        except Exception as e:
            print(f"Error general {e}")                            
        
                       
        
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
            ruta_archivo_local = f"/root/Inventarios/{self.hostname}-software.txt"
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
        try:                        
            self.conexionSSH = paramiko.SSHClient()            
            self.conexionSSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())            
            mensaje = f"Intentando Realizar conexion a {self.hostname} con el usuario {self.username}."
            self.registrarLog(mensaje,"INF",self.rutaArchivo,self.hostname)
            self.conexionSSH.connect(hostname=self.hostname,port=self.port,timeout=15,username=self.username,key_filename=self.keyfile,passphrase=self.passphrase)                                    
            transport = self.conexionSSH.get_transport()
            if transport:
                transport.set_keepalive(60)
            return True , self.rutaArchivo                   
        except paramiko.AuthenticationException as sshE:            
            mensaje = f"Error al establecer conexion SSH a host {self.hostname} al usuario {self.username}"
            self.registrarLog(mensaje,"ERR",self.rutaArchivo,self.hostname)
            if self.conexionSSH:
                self.conexionSSH.close()
            return False , self.rutaArchivo            
        except Exception as e:
            mensaje = f"Ocurrio un error inesperado : {e}"
            self.registrarLog(mensaje,"ERR",self.rutaArchivo,self.hostname)
            if self.conexionSSH:
                self.conexionSSH.close()
            return False , self.rutaArchivo
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
        rutaInicial = f"/backupcolaboradores/Backup/{self.hostname}/"
        listaRutasLocales = []                
        os.makedirs(rutaInicial,exist_ok=True)
        for carpetas in listaCarpetas:
            print(f"Creando{carpetas}")
            ruta = Path(rutaInicial)/carpetas
            os.makedirs(ruta,exist_ok=True)
            print(f"Esto se creo {ruta}")        
            listaRutasLocales.append(ruta)
            mensaje = "Las carpetas iniciales en el Disco /backupcolaboradores/ fueron creadas con exito"
            self.registrarLog(mensaje,"INF",self.rutaArchivo,self.hostname)
        return listaRutasLocales
    
    
    def creaRutasRemotas(self,usuario:str,listaRutaLocales:list):        
        lsRutaBKUP = []
        rBaseRemoC = "C:/Users/"        
        try:
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
                    ruta ="D:/"
                    local = Path(rLocal)/"Disco_D"
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
            
            
            
    def realizarBKUP(self,rBaseRemo:str,rBaseLocal:str,nombreCarpeta:str):
        if nombreCarpeta != "":
            rBaseRemoR = f"{rBaseRemo}/{nombreCarpeta}"
            rBaseLocalR = f"{rBaseLocal}/{nombreCarpeta}"
        else:
            rBaseRemoR = rBaseRemo
            rBaseLocalR = rBaseLocal        
        try:                
            listaArchivos = list(self.canalSFTP.listdir_iter(rBaseRemoR))
            nombreArchivo = ""         
            for archivo in listaArchivos:            
                nombreArchivo = archivo.filename
                if stat.S_ISDIR(archivo.st_mode):                    
                    creaRutaLocal = f"{rBaseLocalR}/{nombreArchivo}"
                    os.makedirs(creaRutaLocal,exist_ok=True)
                    mensaje = f"Se creo la carpeta {nombreCarpeta}"
                    self.registrarLog(mensaje,"INF",self.rutaArchivo,self.hostname)                                                            
                    self.realizarBKUP(rBaseRemoR,rBaseLocalR,nombreArchivo)                                            
                else:                            
                    rutaCopiarLocal = f"{rBaseLocalR}/{nombreArchivo}"
                    rutaCopiarRemoto = f"{rBaseRemoR}/{nombreArchivo}"                    
                    existeLocal = os.path.exists(rutaCopiarLocal)
                    try:
                        if not existeLocal:
                            mensaje = f"Copiando archivo {nombreArchivo}"
                            self.registrarLog(mensaje,"INF",self.rutaArchivo,self.hostname)             
                            mensaje = f"De {rutaCopiarRemoto} --> {rutaCopiarLocal}"
                            self.registrarLog(mensaje,"INF",self.rutaArchivo,self.hostname)                                                        
                            self.canalSFTP.get(rutaCopiarRemoto,rutaCopiarLocal)
                            mensaje = f"Archivo {nombreArchivo} salvado con EXITO"
                            self.registrarLog(mensaje,"INF",self.rutaArchivo,self.hostname)             
                        else:    
                            tamañoRemoto = archivo.st_size
                            tamañoLocal = os.path.getsize(rutaCopiarLocal)                            
                            if tamañoRemoto != tamañoLocal:
                                mensaje = f"Copiando archivo {nombreArchivo}"
                                self.registrarLog(mensaje,"INF",self.rutaArchivo,self.hostname)             
                                mensaje = f"De {rutaCopiarRemoto} --> {rutaCopiarLocal}"
                                self.registrarLog(mensaje,"INF",self.rutaArchivo,self.hostname)                                                        
                                self.canalSFTP.get(rutaCopiarRemoto,rutaCopiarLocal)
                                mensaje = f"Archivo {nombreArchivo} salvado con EXITO"
                                self.registrarLog(mensaje,"INF",self.rutaArchivo,self.hostname)
                            else:
                                mensaje = f"El archivo {nombreArchivo} ya fue guardado de manera local"
                                self.registrarLog(mensaje,"INF",self.rutaArchivo,self.hostname)             
                    except FileNotFoundError as e:                        
                        print(f"Error posiblemente el archivo no existe : {e} -{rutaCopiarRemoto}")
                        mensaje = f"Error posiblemente el archivo no existe : {e} -{rutaCopiarRemoto}"
                        self.registrarLog(mensaje,"ERR",self.rutaArchivo,self.hostname)                        
                    except Exception as e:                        
                        print(f"Ocurrio un error inesperado : {e} bucle 1 -{rutaCopiarRemoto}")
                        mensaje = f"Ocurrio un error inesperado : {e} -{rutaCopiarRemoto}"
                        self.registrarLog(mensaje,"ERR",self.rutaArchivo,self.hostname)                                                                                                                                               
        except SFTPError as e:            
            print(f"Error en la carpeta {rBaseRemoR} posiblemente no existe : {e}")
            mensaje = f"Error en la carpeta {rBaseRemoR} posiblemente no existe : {e}"
            self.registrarLog(mensaje,"ERR",self.rutaArchivo,self.hostname)
            if self.canalSFTP:
                self.canalSFTP.close()
            if self.conexionSSH:
                self.conexionSSH.close()                  
        except FileExistsError as e:            
            print(f"Error en ruta {rBaseRemoR} posiblemente no existe : {e}")
            mensaje = f"Error en ruta {rBaseRemoR} posiblemente no existe : {e}"
            self.registrarLog(mensaje,"ERR",self.rutaArchivo,self.hostname)                              
            if self.canalSFTP:
                self.canalSFTP.close()
            if self.conexionSSH:
                self.conexionSSH.close()
        except Exception as e:                        
            print(f"Ocurrio un error inesperado {e} - {rBaseRemoR} - {rBaseLocalR}")
            mensaje = f"Ocurrio un error inesperado {e} - {rBaseRemoR} - {rBaseLocalR}"
            self.registrarLog(mensaje,"ERR",self.rutaArchivo,self.hostname) 
            if self.canalSFTP:
                self.canalSFTP.close()
            if self.conexionSSH:
                self.conexionSSH.close()                            
                
    def cerrarConexiones(self):
        self.canalSFTP.close()
        self.conexionSSH.close()