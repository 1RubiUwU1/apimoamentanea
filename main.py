from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # habilita CORS para cualquier origen

# Ruta para comprobar que la API está viva
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "ok", "message": "API funcionando"})


# Ruta para transcripción
@app.route("/transcribe", methods=["POST", "GET"])
def transcribe():
    try:
        audio_data = None

        # Si viene por POST como archivo
        if request.method == "POST":
            if "file" not in request.files:
                return jsonify({"error": "No se envió archivo"}), 400

            file = request.files["file"]
            audio_data = file.read()

        # Si viene por GET con URL del audio
        elif request.method == "GET":
            audio_url = request.args.get("url")
            if not audio_url:
                return jsonify({"error": "No se envió parámetro url"}), 400

            # Descargamos el archivo desde la URL
            resp = requests.get(audio_url)
            if resp.status_code != 200:
                return jsonify({"error": "No se pudo descargar el audio"}), 400

            audio_data = resp.content

        # Simulación de transcripción (aquí va tu modelo/servicio real)
        # Por ejemplo, podrías conectar con OpenAI Whisper, SpeechRecognition, etc.
        texto = "Transcripción simulada del audio recibido."

        return jsonify({
            "status": "ok",
            "text": texto,
            "size_bytes": len(audio_data)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
