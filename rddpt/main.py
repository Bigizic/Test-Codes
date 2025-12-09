#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from ext_aud_vid import extract_audio
from aud_txt import transcribe_audio
from txt_lng import translate_text
from final import speak_text

load_dotenv()

if __name__ == "__main__":
    video_file = "vid_1.MP4"
    original_language = "ha" # in ISO-639-1 code
    final_language = "English"  # desired output for translation
    
    try:
        # extract audio
        audio_path = extract_audio(video_file)
        
        # transcribe audio
        transcribed_text = transcribe_audio(audio_path, language=original_language)
        print(f"\n--- transcribed text ---\n{transcribed_text}\n------------------------\n")
        
        # translate text
        translated_text = translate_text(transcribed_text, final_language)
        print(f"\n--- translated text ({final_language}) ---\n{translated_text}\n-----------------------------------\n")
        
        # speak text
        speak_text(translated_text)
        
    except Exception as e:
        print(f"an error occurred: {e}")
        exit(1)
