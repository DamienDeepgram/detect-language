import wave
import tempfile
import argparse
from flask import Flask, request, jsonify
from openai import OpenAI

client = OpenAI()
app = Flask(__name__)

def trim_audio_to_15_seconds(input_path):
    """
    Trim the audio file to the first 15 seconds if it is longer.

    Parameters:
        input_path (str): Path to the input WAV file.

    Returns:
        str: Path to the trimmed WAV file.
    """
    with wave.open(input_path, 'rb') as wav:
        params = wav.getparams()
        frame_rate = params.framerate
        n_channels = params.nchannels
        sampwidth = params.sampwidth

        max_frames = frame_rate * 15
        n_frames = min(wav.getnframes(), max_frames)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            with wave.open(tmp_file.name, 'wb') as trimmed_wav:
                trimmed_wav.setnchannels(n_channels)
                trimmed_wav.setsampwidth(sampwidth)
                trimmed_wav.setframerate(frame_rate)
                trimmed_wav.writeframes(wav.readframes(n_frames))

            return tmp_file.name

def detect_language_with_whisper(wav_file_path):
    """
    Use OpenAI's Whisper API to detect the language of a WAV file.

    Parameters:
        wav_file_path (str): Path to the WAV file to process.

    Returns:
        str: Detected language code or an error message.
    """
    try:
        trimmed_wav_path = trim_audio_to_15_seconds(wav_file_path)
        with open(trimmed_wav_path, "rb") as wav_file:
            response = client.audio.transcriptions.create(
                file=wav_file,
                model="whisper-1",
                response_format="verbose_json"
            )

            print(response)

            if hasattr(response, 'language'):
                return response.language
            else:
                return "Language detection failed."

    except FileNotFoundError:
        return "Error: WAV file not found."
    except Exception as e:
        return f"Error: Failed to communicate with the API. {str(e)}"

@app.route('/detect-language', methods=['POST'])
def api_detect_language():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        file.save(tmp_file.name)
        detected_language = detect_language_with_whisper(tmp_file.name)
        return jsonify({"detected_language": detected_language})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect language using OpenAI's Whisper API.")
    parser.add_argument("file", type=str, nargs="?", help="Path to the WAV file to process.")
    parser.add_argument("--serve", action="store_true", help="Run as a Flask API server.")
    args = parser.parse_args()

    if args.serve:
        app.run(host="0.0.0.0", port=5000)
    elif args.file:
        detected_language = detect_language_with_whisper(args.file)
        print(f"Detected Language: {detected_language}")
    else:
        print("Error: Please provide a file path or use --serve to run as a server.")
