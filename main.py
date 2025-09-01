# transcripter_api.py
from flask import Flask, request, jsonify
from flask_cors import CORS  # 🔹 Importar CORS
from pydub import AudioSegment
import speech_recognition as sr
import os
import tempfile

app = Flask(__name__)
CORS(app)  # 🔹 Habilitar CORS para todos los dominios

@app.route("/transcripter", methods=["POST"])
def transcribe():
    if "file" not in request.files:
        return jsonify({"error": "No se proporcionó archivo de audio"}), 400

    audio_file = request.files["file"]

    try:
        # Guardar temporalmente el archivo recibido
        temp_ogg = tempfile.NamedTemporaryFile(delete=False, suffix=".ogg")
        audio_file.save(temp_ogg.name)

        # Convertir OGG a WAV mono 16kHz
        temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        audio = AudioSegment.from_file(temp_ogg.name)
        audio = audio.set_channels(1).set_frame_rate(16000)
        audio.export(temp_wav.name, format="wav")

        # Reconocimiento de voz
        r = sr.Recognizer()
        with sr.AudioFile(temp_wav.name) as source:
            audio_data = r.record(source)
        try:
            text = r.recognize_google(audio_data, language="es-ES")
        except sr.UnknownValueError:
            text = "No se pudo transcribir el audio"
        except sr.RequestError as e:
            text = f"Error de servicio: {e}"

        # Limpiar archivos temporales
        os.unlink(temp_ogg.name)
        os.unlink(temp_wav.name)

        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
