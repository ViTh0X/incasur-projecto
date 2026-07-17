from django.core.mail import send_mail

def enviar_correo_ti_incasur(mensaje:str,asunto:str):
    send_mail(
        subject=asunto,
        message=mensaje,
        from_email='lquispe@cajaincasur.com.pe',
        recipient_list=['ti@cajaincasur.com.pe'],
        fail_silently=False,
    )