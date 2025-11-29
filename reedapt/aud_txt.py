from openai import OpenAI
import os

def transcribe_audio(audio_path, language=None):
    """
    transcribe audio to text using OpenAI's Whisper model.
    """

    if not language:
        raise ValueError("language must be specified")
    
    client = OpenAI()
    
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"audio file not found: {audio_path}")

    print(f"transcribing audio from {audio_path}...")
    
    with open(audio_path, "rb") as audio_file:
        kwargs = {
            "model": "whisper-1",
            "file": audio_file,
        }
        
        transcription = client.audio.translations.create(**kwargs)
    
    print("transcription successful!")
    return transcription.text
