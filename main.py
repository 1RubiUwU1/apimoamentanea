from flask import Flask, request, jsonify
from flask_cors import CORS
import speech_recognition as sr
from pydub import AudioSegment
import os
import tempfile
import traceback

app = Flask(__name__)
CORS(app)

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "file" not in request.files:
        return jsonify({"error": "No se envió archivo"}), 400
    
    file = request.files["file"]

    try:
        # Guardar temporalmente el archivo recibido
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as temp_in:
            file.save(temp_in.name)
            input_path = temp_in.name

        # Convertir OGG a WAV
        wav_path = input_path.replace(".ogg", ".wav")
        audio = AudioSegment.from_file(input_path, format="ogg")
        audio = audio.set_channels(1).set_frame_rate(16000)
        audio.export(wav_path, format="wav")

        # Transcripción
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="es-ES")

        # Limpiar temporales
        os.remove(input_path)
        os.remove(wav_path)

        return jsonify({"text": text})

    except Exception as e:
        # 👇 Esto imprimirá el error real en la consola
        print("❌ ERROR en transcripción:", str(e))
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
