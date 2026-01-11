"""
Yoruba language configuration
"""

DISPLAY_NAME = "Yoruba"
LANGUAGE_CODE = "yo"

# Use Whisper or custom model for transcription
USE_WHISPER = True

# Use Hugging Face NLLB-200 for translation (best for Yoruba)
USE_HUGGINGFACE_TRANSLATE = True
USE_GOOGLE_TRANSLATE = False
USE_SPITCH_TRANSLATE = False

# Use Hugging Face Coqui XTTS-v2 or MMS TTS for TTS (best quality for Yoruba)
USE_HUGGINGFACE_TTS = True
USE_ELEVENLABS = False
USE_SPITCH_TTS = False

