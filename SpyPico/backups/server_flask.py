from flask import Flask, request, jsonify
from data_extraction import regex
from insert import insert_into_db
import os
from backend.models import Imagen, Maquina  # Importamos el modelo Imagen

app = Flask(__name__)

# Ruta donde se guardarán los datos
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Recibir `$cont` como texto plano
@app.route('/receive_text', methods=['PUT'])
def receive_text():
    try:
        text_data = request.data.decode('utf-8', errors='ignore')
        print(text_data)
        datos = regex(text_data)  # return data
        print(datos)
        insert_into_db(datos)
        return jsonify({"status": "Texto recibido correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Recibir imágenes
@app.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        image_data = request.data  # Recibir la imagen en binario
        file_path = os.path.join(UPLOAD_FOLDER, f"image_{len(os.listdir(UPLOAD_FOLDER)) + 1}.jpg")

        # Guardar la imagen en el sistema de archivos
        with open(file_path, "wb") as f:
            f.write(image_data)

        print(f"Imagen guardada en {file_path}")

        # Guardar la imagen en la base de datos en el modelo Imagen
        # Asegúrate de obtener el ID correcto de la máquina
        maquina_id = 1  # Cambia esto al ID de la máquina correcta

        # Crear la instancia en la base de datos para Imagen
        imagen = Imagen(maquina_id=maquina_id, imagen=image_data)  # Guarda la imagen en binario
        imagen.save()

        return jsonify({"status": "Imagen recibida y almacenada correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Recibir archivos `login_data` (SQLite)
@app.route('/<filename>', methods=['PUT'])
def upload_file(filename):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        with open(file_path, "wb") as f:
            f.write(request.data)
        print(f"Archivo {filename} recibido y guardado correctamente.")
        return jsonify({"status": f"Archivo {filename} recibido correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8082)
