import os
from datetime import datetime
from django.conf import settings

class logArchivos():   
            
    def crearArchivo(self,host:str):        
        rutaBaseLog = f"/mnt/backupcolaboradores/Logs/{host}"
        os.makedirs(rutaBaseLog,exist_ok=True)
        dd = datetime.now().day
        mm =  datetime.now().month
        yyyy = datetime.now().year        
        rutaArchivo = f"{rutaBaseLog}/Log-{host}-{yyyy}-{mm}-{dd}.txt"
        
        with open(rutaArchivo,'w') as archivoLog:
            titulo = f"***********LOG DE BACKP UP HOST (IP): {host} FECHA {yyyy} - {mm}\n"
            archivoLog.write(titulo)        
        return rutaArchivo   
    
    
    def registrarLog(self,mensaje:str,tipo:str,rutaArchivo:str,host:str):              
        time = datetime.now()
        with open(rutaArchivo,'a') as archivoLog:
            mensaje = f"{time} - {host} - {tipo} - {mensaje}\n"
            archivoLog.write(mensaje)

    def verificar_archivos_logs(self,host:str):
        termino_con_errores = False
        rutaBaseLog = f"/mnt/backupcolaboradores/Logs/{host}"
        dd = datetime.now().day        
        mm =  datetime.now().month
        yyyy = datetime.now().year
        rutaArchivo_buscado = f"{rutaBaseLog}/Log-{host}-{yyyy}-{mm}-{dd}.txt"
        nombre_archivo = f"LogErrores-{host}.txt"        
        nombre_archivo_err = os.path.join(settings.MEDIA_ROOT,'logs_errores',nombre_archivo)
        with open(nombre_archivo_err,'w') as archivo_log_errores:
            pass
        with open(rutaArchivo_buscado,'r') as archivo_errores:
            for linea in archivo_errores:
                if "- ERR -" in  linea:
                    with open(nombre_archivo_err,'a') as archivo_log_errores:
                        mensaje = linea
                        archivo_log_errores.write(mensaje)
        if os.path.getsize(nombre_archivo_err) == 0:
            return termino_con_errores
        else:
            termino_con_errores = True
            return termino_con_errores
                