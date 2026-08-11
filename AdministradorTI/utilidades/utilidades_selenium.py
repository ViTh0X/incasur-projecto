from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

import time
from dotenv import load_dotenv
import os
load_dotenv()

import secrets
import string

from .utilidades_qr import crear_qr_wifi
from .envio_correo import enviar_correo_cambio_contraseña, fallo_crear_contraseña

URL_EQUIPO_WIFI = "http://192.168.40.150:8080"
USUARIO = "Admin"
CONTRASEÑA = os.getenv('CONTRASENA_WIFI')
ruta_almacenamiento_imagen_qr = os.getenv('RUTAQR')


def  crear_contrasena():
    caracteres = string.ascii_letters + string.digits
    mitad1 = ''.join(secrets.choice(caracteres) for _ in range(4))
    mitad2 = ''.join(secrets.choice(caracteres) for _ in range(3))
    contrasena = f"{mitad1}@{mitad2}"
    return contrasena

    
def cambiar_contrasena_wifi():
    #Ingresamos al equipo wifi dlink
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new") # <-- Activa el modo headless moderno
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080") # <-- Recomendado para evitar problemas de clicks en elementos ocultos
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36") # Opcional: evita bloqueos
        chrome_options.add_argument("--no-sandbox") # Crucial en entornos Linux o si el proceso corre como root/servicios
        chrome_options.add_argument("--disable-dev-shm-usage") # Evita que Chrome colapse por falta de memoria compartida (/dev/shm) en el servidor
        # Se pasan las options al inicializar el driver
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), 
            options=chrome_options
        )
        
        driver.get(URL_EQUIPO_WIFI)
    except Exception as e:
        print(f"Error al inicializar el WebDriver: {e}")
        exit()
    # Acceder al equipo usuario contraseña
    try:
        campo_contraseña = driver.find_element(By.ID, "loginpwd")
        boton_iniciar_sesion = driver.find_element(By.ID, "noGAC")
        campo_contraseña.send_keys(CONTRASEÑA)
        boton_iniciar_sesion.click()
        time.sleep(2)
        print("Acceso al equipo wifi exitoso.")
    except Exception as e:
        print(f"Error al acceder al equipo wifi: {e}")
        driver.quit()
        exit()
    # Accedemos a la configuracion de wifi
    try:
        link_parametros_inalambricos = driver.find_element(By.LINK_TEXT, "PARÁMETROS INALÁMBRICOS")
        link_parametros_inalambricos.click()
        boton_configuracion_wifi = driver.find_element(By.ID, "inetsetup")
        boton_configuracion_wifi.click()
        time.sleep(2)
        print("Acceso a la configuración de WiFi exitoso.")
    except Exception as e:
        print(f"Error al acceder a la configuración de WiFi: {e}")
        driver.quit()
        exit()
    #Cambiamos la contraseña 
    try:
        campo_contraseña_wifi = driver.find_element(By.ID, "wpa_psk_key")
        nueva_contraseña = crear_contrasena()
        campo_contraseña_wifi.clear()
        campo_contraseña_wifi.send_keys(nueva_contraseña)
        campo_confirmar_contraseña_wifi = driver.find_element(By.XPATH, "//input[@value='Guardar parámetros']")
        campo_confirmar_contraseña_wifi.click()
        time.sleep(5)
        qr_generado_ruta = crear_qr_wifi(contraseña_wifi=nueva_contraseña,ruta_qr=ruta_almacenamiento_imagen_qr)
        if not qr_generado_ruta:
            enviar_correo_cambio_contraseña(
                mensaje=f"Se ha cambiado la contraseña de WiFi a: {nueva_contraseña}",
                asunto="Cambio de Contraseña WiFi",
                ruta_imagen=qr_generado_ruta
            )
        else:
            fallo_crear_contraseña(asunto="FALLO GENERAR QR WIFI",mensaje="Fallo al generar QR wifi de la sala de reuniones")
            print("Error al generar el código QR.")
        print("Contraseña de WiFi cambiada y código QR generado exitosamente.")
    except Exception as e:
        print("Ocurrio un error al generar el QR , no se logro.")
        driver.quit()
        exit()
        

        
        