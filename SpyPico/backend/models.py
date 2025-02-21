from django.db import models

class Maquina(models.Model):
    nombre = models.CharField(max_length=255)
    sistema_operativo = models.CharField(max_length=255, null=True, blank=True)
    version_sistema = models.CharField(max_length=255, null=True, blank=True)
    fabricante = models.CharField(max_length=255, null=True, blank=True)
    modelo = models.CharField(max_length=255, null=True, blank=True)
    ip_publica = models.GenericIPAddressField(null=True, blank=True)
    dominio = models.CharField(max_length=255, null=True, blank=True)
    tiempo_de_infeccion_fecha = models.DateField(null=True, blank=True)
    tiempo_de_infeccion_hora = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.nombre

# Principalmente trabajaremos con la una relacion de muchos a uno en cada tabla referente a 'maquina'
# para mantener un identificador unico en acada registro con la llave foranea 
 

class Imagen(models.Model):
    maquina = models.ForeignKey(Maquina, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.BinaryField()  # Guarda la imagen en binario

class Archivo(models.Model):
    maquina = models.ForeignKey(Maquina, related_name='archivos', on_delete=models.CASCADE)
    archivo = models.BinaryField()  
    nombre = models.CharField(max_length=255, blank=True, null=True)

class Usuario(models.Model):
    maquina = models.ForeignKey(Maquina, related_name='usuarios', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    estado = models.BooleanField() 

    def __str__(self):
        return self.nombre

class Red(models.Model):
    maquina = models.ForeignKey(Maquina, related_name='redes', on_delete=models.CASCADE)
    interfaz = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()

    def __str__(self):
        return self.interfaz

class Wifi(models.Model):
    maquina = models.ForeignKey(Maquina, related_name='wifis', on_delete=models.CASCADE)
    ssid = models.CharField(max_length=255, null=True, blank=True)
    clave = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.ssid

class Password(models.Model):
    maquina = models.ForeignKey(Maquina, related_name='contraseñas', on_delete=models.CASCADE)
    clave_base64 = models.TextField()

    def __str__(self):
        return self.clave_base64
