from flask import Flask, request, jsonify
from data_extraction import regex
from insert import insert_into_db
from backend.models import Imagen, Maquina, Archivo 
import os
import time
app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Recibir `$cont` como texto plano
@app.route('/receive_text', methods=['PUT'])
def receive_text():
    try:
        text_data = request.data.decode('utf-8', errors='ignore')
        #print(text_data)
        datos = regex(text_data)  
       # print(datos)
        insert_into_db(datos)  
        return jsonify({"status": "Texto recibido correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Recibir imágenes
@app.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        image_data = request.data  

        maquina = Maquina.objects.order_by('-id').first()  # Obtener la máquina más reciente por id

        if not maquina:
            return jsonify({"error": "No se encontró la máquina para asociar la imagen"}), 400

        imagen = Imagen(maquina=maquina, imagen=image_data)
        imagen.save()

        return jsonify({"status": "Imagen almacenada correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Recibir archivos login_data (SQLite)
@app.route('/upload_file/<path:filename>', methods=['PUT'])
def upload_file(filename):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        with open(file_path, "wb") as f:
            f.write(request.data)
        print(f"Archivo {filename} recibido y guardado correctamente.")
        return jsonify({"status": f"Archivo {filename} recibido correctamente"}), 200
    except Exception as e:
        return jsonify({"error": "Ocurrió un error"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8082)
