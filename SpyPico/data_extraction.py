import re, json


def regex(texto,imagenes=None, archivos=None):
    data = {
        "Maquina": {},
        "Usuarios": {},
        "Redes": [],
        "IP_Publica": "",
        "Redes_WiFi": [],
        "Clave_Base64": "",
        "Imagenes":[],
        "Archivos":[],
    }

    # Expresiones regulares
    regex_sistema = re.compile(r"^(?:OS Name|Nombre del sistema operativo):\s*(.*)")
    regex_version = re.compile(r"^(?:OS Version|Versi\u00f3n del sistema operativo):\s*(.*)")
    regex_fabricante = re.compile(r"^(?:System Manufacturer|Fabricante del sistema):\s*(.*)")
    regex_modelo = re.compile(r"^(?:System Model|Modelo del sistema):\s*(.*)")
    regex_dominio = re.compile(r"^(?:Domain|Dominio):\s*(.*)")
    regex_whoami = re.compile(r"^whoami:\s*(.*)")
    regex_usuario = re.compile(r"^(.*)\s+(True|False)$")
    regex_redes = re.compile(r"^Interfaz: (.*?) - IP: (\d+\.\d+\.\d+\.\d+)")
    regex_ip_publica = re.compile(r"^IP PUBLICA:\s*(.*)")
    regex_wifi = re.compile(r"^(.*) : (.*)$")
    regex_clave = re.compile(r"PASSWORD: (.+)")
    regex_imagen = re.compile(r"Imagen:\s*(.*\.jpg|.*\.png|.*\.jpeg)")
    regex_archivo = re.compile(r"Archivo:\s*(.*\.\w+)")

    for line in texto.splitlines():
        line = line.strip()

        # Sistema
        if match := regex_sistema.match(line):
            data["Maquina"]["Nombre del sistema operativo"] = match.group(1)
        elif match := regex_version.match(line):
            data["Maquina"]["Versi\u00f3n del sistema operativo"] = match.group(1)
        elif match := regex_fabricante.match(line):
            data["Maquina"]["Fabricante del sistema"] = match.group(1)
        elif match := regex_modelo.match(line):
            data["Maquina"]["Modelo del sistema"] = match.group(1)
        elif match := regex_dominio.match(line):
            data["Maquina"]["Dominio"] = match.group(1)
        elif match := regex_whoami.match(line):
            data["Maquina"]["whoami"] = match.group(1)

        # Usuarios
        elif match := regex_usuario.match(line):
            user, state = match.groups()
            data["Usuarios"][user.strip()] = state

        # IP P\u00fablica
        elif match := regex_ip_publica.match(line):
            data["IP_Publica"] = match.group(1)

        # Redes
        elif match := regex_redes.match(line):
            interface, ip = match.groups()
            data["Redes"].append({"Interfaz": interface.strip(), "IP": ip})

        # Contrase\u00f1as WiFi
        elif match := regex_wifi.match(line):
            network, password = match.groups()
            data["Redes_WiFi"].append({"SSID": network.strip(), "Clave": password.strip()})

        # Clave en Base64
        elif match := regex_clave.match(line):
            data["Clave_Base64"] = match.group(1)

        # Captura imágenes
    if imagenes:
       for imagen in imagenes:
           data["Imagenes"].append(imagen)

    #    # Captura archivos
    if archivos:
       for archivo in archivos:
           data["Archivos"].append(archivo)
    # Retorna el diccionario con los datos procesados
    return data
