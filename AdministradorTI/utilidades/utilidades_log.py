import os
from datetime import datetime

class logArchivos():   
            
    def crearArchivo(self,host:str):        
        rutaBaseLog = f"D:/Logs/{host}"
        os.makedirs(rutaBaseLog,exist_ok=True)
        mm =  datetime.now().month
        yyyy = datetime.now().year
        rutaArchivo = f"{rutaBaseLog}/Log-{host}-{yyyy}-{mm}.txt"
        
        with open(rutaArchivo,'w') as archivoLog:
            titulo = f"***********LOG DE BACKP UP HOST (IP): {host} FECHA {yyyy} - {mm}\n"
            archivoLog.write(titulo)        
        return rutaArchivo   
    
    
    def registrarLog(self,mensaje:str,tipo:str,rutaArchivo:str,host:str):              
        time = datetime.now()
        with open(rutaArchivo,'a') as archivoLog:
            mensaje = f"{time} - {host} - {tipo} - {mensaje}\n"
            archivoLog.write(mensaje)