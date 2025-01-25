from flask import Flask
from flask_cors import CORS
from routes.image_routes import image_route


app = Flask(__name__)
CORS(app)


# Registrar rutas
app.register_blueprint(image_route, url_prefix="/api/image")


@app.route("/ping", methods=["GET"])
def ping():
    return {"message": "server is running"}, 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)