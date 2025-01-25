from flask import Blueprint, request, jsonify, send_file
from modules.image_processor import BackgroundRemover
from config import OUTPUT_FOLDER_IMAGE, allowedFile
import gc

image_route = Blueprint("image_routes", __name__)
remover = BackgroundRemover(OUTPUT_FOLDER_IMAGE)

@image_route.route("/remove-bg", methods=["POST"])
def removeBg():

    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    image_file = request.files['image']
    if not allowedFile(image_file.filename):
        return jsonify({"error": "Invalid file type"}), 400
    
    try:
        output_path = remover.processImage(image_file)
        return send_file(output_path, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        gc.collect()

@image_route.route("/prueba", methods=["GET"])
def pruebRoute():
    return jsonify({"message": "prueba"}), 200