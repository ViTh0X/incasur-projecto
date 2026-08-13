import qrcode


def crear_qr_wifi(contraseña_wifi,ruta_qr):
    try:
    # Configura los datos de tu red Wi-Fi no oculta
        ssid = "REUINCASURWIFI"
        password = contraseña_wifi
        security = "WPA"
        is_hidden = False  # Indicamos que la red no emite su SSID

        # Formateamos la cadena incluyendo el flag H:true
        hidden_flag = "H:true;" if is_hidden else ""
        wifi_data = f"WIFI:S:{ssid};T:{security};P:{password};{hidden_flag};"

        # Crear y guardar la imagen del QR
        qr_img = qrcode.make(wifi_data)
        ruta_qr_final = f"{ruta_qr}/wifi_qr.png"
        qr_img.save(ruta_qr_final)
        return True,ruta_qr_final
    except Exception as e:
        return False,e