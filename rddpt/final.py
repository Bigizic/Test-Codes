from elevenlabs.client import ElevenLabs
from elevenlabs import save

import os

def speak_text(text):
    """
    convert text to speech using ElevenLabs and saves it to 'saved/output.mp3'.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY not found")
    
    elevenlabs = ElevenLabs(
        api_key=api_key,
    )
    
    # ensures saved directory exists
    os.makedirs("saved", exist_ok=True)
    
    print("generating speech...")
    
    audio = elevenlabs.text_to_speech.convert(
        text=text,
        voice="Bella", # change voice here
        model="eleven_monolingual_v1"
    )
    
    output_path = os.path.join("saved", "output.mp3")
    print(f"saving speech to {output_path}...")
    save(audio, output_path)
    print("audio saved successfully!")
