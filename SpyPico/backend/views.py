from django.shortcuts import render
from .models import Maquina, Usuario, Red, Wifi, Password, Imagen, Archivo
import base64

def consultas (request):
    objeto = Maquina.objects.all()
    return render (request, 'consulta.html', {'maquinas':objeto})


def detalles_maquina(request, parametro):
    maquina = Maquina.objects.filter(nombre=parametro).first()
    
    if not maquina:
        return render(request, 'error.html', {'mensaje': 'Máquina no encontrada.'})

    usuarios = Usuario.objects.filter(maquina=maquina)
    redes = Red.objects.filter(maquina=maquina)
    wifies = Wifi.objects.filter(maquina=maquina)
    password = Password.objects.filter(maquina=maquina).first()

    # Obtener imágenes directamente desde la BD y convertirlas a base64
    imagenes = Imagen.objects.filter(maquina=maquina)
    imagenes_base64 = [base64.b64encode(imagen.imagen).decode('utf-8') for imagen in imagenes]

    archivos = Archivo.objects.filter(maquina=maquina)
    print(maquina.nombre)
    print("Archivos encontrados:", maquina)
    contexto = {
        'maquina': maquina,
        'parametro': parametro,
        'usuarios': usuarios,
        'redes': redes,
        'wifies': wifies,
        'password': password,
        'imagenes_base64': imagenes_base64,
        'archivos': archivos, 
    }
    return render(request, 'detalles_m.html', contexto)



def descargar_archivo(request, archivo_id):
    archivo = Archivo.objects.get(id=archivo_id)

    # Suponiendo que 'archivo.archivo' contiene los datos binarios del archivo
    response = HttpResponse(archivo.archivo, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{archivo.archivo.name}"'
    
    return response
