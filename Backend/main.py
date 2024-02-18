from uuid import uuid4
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from moviepy.audio.AudioClip import concatenate_audioclips
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.config import change_settings
from tiktokvoice import *
from utils import *

# Load environment variables
load_dotenv("../.env")

# Set environment variables
SESSION_ID = os.getenv("TIKTOK_SESSION_ID")
change_settings({"IMAGEMAGICK_BINARY": os.getenv("IMAGEMAGICK_BINARY")})

# Initialize Flask
app = Flask(__name__)
CORS(app)

# Constants
HOST = "0.0.0.0"
PORT = 8080
AMOUNT_OF_STOCK_VIDEOS = 10
GENERATING = False


@app.route("/api/render-voice-sample/<voice>", methods=["GET"])
def renderVoiceSample(voice):
    return jsonify(
        {
            "status": "success",
            "message": "Video generated! See temp/output.mp4 for result.",
            "data": generate_audio_base64("Hello, how are you doing", voice)
        }
    )


# Generation Endpoint
@app.route("/api/generate", methods=["POST"])
def generate():
    try:
        # Set global variable
        global GENERATING
        GENERATING = True

        # Clean
        clean_dir("../temp/")
        clean_dir("../subtitles/")

        # Parse JSON
        data = request.get_json()

        # Print little information about the video which is to be generated
        print(colored("[Video to be generated]", "blue"))
        print(colored("   Subject: " + data["videoSubject"], "blue"))

        if not GENERATING:
            return jsonify(
                {
                    "status": "error",
                    "message": "Video generation was cancelled.",
                    "data": [],
                }
            )

        # Generate a script
        script = data["videoSubject"]
        voice = data["voice"]

        if not voice:
            print(colored("[!] No voice was selected. Defaulting to \"en_us_001\"", "yellow"))
            voice = "en_us_001"

        # Let user know
        print(colored("[+] Script generated!\n", "green"))

        if not GENERATING:
            return jsonify(
                {
                    "status": "error",
                    "message": "Video generation was cancelled.",
                    "data": [],
                }
            )

        # Split script into sentences
        sentences = script.split(". ")
        # Remove empty strings
        sentences = list(filter(lambda x: x != "", sentences))
        paths = []
        # Generate TTS for every sentence
        for sentence in sentences:
            if not GENERATING:
                return jsonify(
                    {
                        "status": "error",
                        "message": "Video generation was cancelled.",
                        "data": [],
                    }
                )
            current_tts_path = f"../temp/{uuid4()}.mp3"
            tts(sentence, voice, filename=current_tts_path)
            audio_clip = AudioFileClip(current_tts_path)
            paths.append(audio_clip)

        # Combine all TTS files using moviepy
        final_audio = concatenate_audioclips(paths)
        tts_path = f"../temp/{uuid4()}.mp3"
        final_audio.write_audiofile(tts_path)
    except Exception as err:
        print(colored(f"[-] Error: {str(err)}", "red"))
        return jsonify(
            {
                "status": "error",
                "message": f"Could not retrieve stock videos: {str(err)}",
                "data": [],
            }
        )


@app.route("/api/cancel", methods=["POST"])
def cancel():
    print(colored("[!] Received cancellation request...", "yellow"))

    global GENERATING
    GENERATING = False

    return jsonify({"status": "success", "message": "Cancelled video generation."})


if __name__ == "__main__":
    app.run(debug=True, host=HOST, port=PORT)
