from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from rembg import remove
import os
from datetime import datetime

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'svg'}

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

output_folder = "output_rembg"

##valida la extencion del archivo
def allowedFile(filename): 
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class BackgroundRemover:
    def __init__(self, output_folder):
        self.output_folder = output_folder

    ## aqui se toma la imagen y se procesa en donde se guardara 
    def processImages(self, image_file):
        today = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        proccessed_folder = os.path.join(self.output_folder, today)
        os.makedirs(proccessed_folder, exist_ok=True)

        originals_folder = os.path.join(proccessed_folder, 'originals')
        os.makedirs(originals_folder, exist_ok=True)


        # Guarda la imagen original
        original_filename = image_file.filename
        ##original_extension = original_filename.rsplit('.', 1)[1].lower()

        # Procesar la imagen recibida
        original_path = os.path.join(originals_folder, original_filename)
        image_file.save(original_path)

        output_path = os.path.join(proccessed_folder, f"output_{original_filename.rsplit('.', 1)[0]}.png")
        self._removeBacklground(original_path, output_path)

        return output_path

    ## metodo para procesar el fondo de la imagen 
    def _removeBacklground(self, input_p, output_p):
        with open(input_p, 'rb') as inp, open(output_p, 'wb') as outp:
            background_output = remove(inp.read())
            outp.write(background_output)


remover = BackgroundRemover(output_folder)


@app.route('/remove-bg', methods=['POST'])
def removeBacklground():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']

    # Validar formato del archivo
    if not allowedFile(image_file.filename):
        return jsonify({"error": "Invalid file format. Only PNG, JPG, JPEG, and SVG are allowed."}), 400


    try:
        output_path = remover.processImages(image_file)
        return send_file(output_path, mimetype='image/png')
    except Exception as e:
        return jsonify({ "error": str(e) }), 500



if __name__ == '__main__':
    app.run(debug=True)