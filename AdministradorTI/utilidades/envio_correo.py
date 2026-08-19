from django.core.mail import send_mail, EmailMessage
import os

def enviar_correo_ti_incasur(mensaje:str,asunto:str):
    send_mail(
        subject=asunto,
        message=mensaje,
        from_email='lquispe@cajaincasur.com.pe',
        recipient_list=['lquispe@cajaincasur.com.pe'],
        fail_silently=False,
    )
    

def enviar_correo_cambio_contraseña(mensaje: str, asunto: str, ruta_imagen: str):
    email = EmailMessage(
        subject=asunto,
        body=mensaje,
        from_email='lquispe@cajaincasur.com.pe',
        to=['lquispe@cajaincasur.com.pe','jrivero@cajaincasur.com.pe','jcornejo@cajaincasur.com.pe'],
    )
    
    # Verificamos que el archivo exista antes de adjuntar
    if os.path.exists(ruta_imagen):
        # Opción A: attach_file asigna el tipo MIME automáticamente
        email.attach_file(ruta_imagen)
    else:
        raise FileNotFoundError(f"No se encontró la imagen en: {ruta_imagen}")

    email.send(fail_silently=False)
    
def fallo_crear_contraseña(mensaje:str,asunto:str):
    send_mail(
        subject=asunto,
        message=mensaje,
        from_email='lquispe@cajaincasur.com.pe',
        recipient_list=['lquispe@cajaincasur.com.pe','jrivero@cajaincasur.com.pe'],
        fail_silently=False,
    )
    