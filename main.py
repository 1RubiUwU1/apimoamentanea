from flask import Flask, request, jsonify
import os
import tempfile
import speech_recognition as sr

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe():
    # Validar archivo
    if "file" not in request.files:
        return jsonify({"error": "No se envió archivo"}), 400

    file = request.files["file"]

    # Crear archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        filepath = tmp.name
        file.save(filepath)

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(filepath) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language="es-ES")
    except sr.UnknownValueError:
        text = "⚠️ No se pudo entender el audio"
    except sr.RequestError as e:
        text = f"⚠️ Error en servicio de reconocimiento: {e}"
    finally:
        # Borrar archivo temporal
        if os.path.exists(filepath):
            os.remove(filepath)

    return jsonify({"text": text})

if __name__ == "__main__":
    # Hacer accesible desde cualquier parte
    app.run(host="0.0.0.0", port=5000)
