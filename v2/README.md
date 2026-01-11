# Dubbing Service V2

Console-based video dubbing application with improved workflow and language-specific processing.

## Features

- **GUI Console**:** Easy-to-use graphical interface for video selection and language configuration
- **Language-Specific Processing**: Each supported language has its own directory with optimized models and tools
- **No API Dependencies**: Standalone application that works without API server
- **Improved Workflow**: Streamlined dubbing pipeline with better error handling

## Supported Languages

- English (en)
- French (fr)
- Spanish (es)
- Yoruba (yo) - Uses Spitch for translation and TTS
- Hausa (ha) - Uses Spitch for translation and TTS
- Igbo (ig) - Uses Spitch for translation and TTS

## Installation

1. Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

2. Set up environment variables (same as original project):
```bash
# Required for translation
export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"

# Required for TTS
export ELEVENLABS_API_KEY="your_elevenlabs_key"

# Required for African languages (Yoruba, Hausa, Igbo)
export SPITCH_API_KEY="your_spitch_key"
```

## Usage

### Running the Console Application

```bash
python v2/main.py
```

Or directly:
```bash
python v2/console.py
```

### Workflow

1. **Select Video**: Click "Browse..." to select your video file
2. **Choose Source Language**: Select the language spoken in the video
3. **Choose Target Language**: Select the language for dubbing
4. **Start Dubbing**: Click "Start Dubbing" to begin the process

The console will display progress and status updates in real-time.

## Architecture

### Directory Structure

```
v2/
├── main.py                 # Entry point
├── console.py              # GUI console application
├── services/               # Core processing services
│   ├── dubbing_processor.py
│   ├── video_processor.py
│   ├── transcription_processor.py
│   ├── translation_processor.py
│   ├── tts_processor.py
│   └── audio_assembler.py
└── languages/              # Language-specific processors
    ├── en/                 # English
    ├── fr/                 # French
    ├── es/                 # Spanish
    ├── yo/                 # Yoruba
    ├── ha/                 # Hausa
    └── ig/                 # Igbo
```

### Processing Pipeline

1. **Audio Extraction**: Extract audio from video file
2. **Audio Separation**: Separate vocals from background using Demucs
3. **Transcription**: Transcribe audio using Whisper or language-specific models
4. **Translation**: Translate text using Google Translate or Spitch
5. **TTS Generation**: Generate speech using ElevenLabs or Spitch
6. **Audio Assembly**: Combine TTS audio with background track
7. **Video Assembly**: Replace original audio with dubbed audio

## Language-Specific Processing

Each language directory can contain:
- `language.py`: Language configuration
- `transcription.py`: Custom transcription processor (optional)
- `translation.py`: Custom translation processor (optional)
- `tts.py`: Custom TTS processor (optional)

If a language-specific processor is not found, the system falls back to default processors (Whisper, Google Translate, ElevenLabs).

## Environment Variables

Same as the original project:
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to Google Cloud credentials
- `ELEVENLABS_API_KEY`: ElevenLabs API key for TTS
- `SPITCH_API_KEY`: Spitch API key for African languages
- `ANTHROPIC_API_KEY`: (Optional) For context processing

## Output

Dubbed videos are saved to:
```
/tmp/v2_dubbing/job_{job_id}/dubbed_video.mp4
```

## Differences from V1

- **No API**: Console-based instead of REST API
- **Simplified Workflow**: Direct processing without queue management
- **Language Directories**: Organized language-specific tools
- **Improved Error Handling**: Better user feedback in console
- **No Database**: Stateless processing (can be added if needed)

## Troubleshooting

### GUI Not Appearing
- Ensure tkinter is installed: `sudo apt-get install python3-tk` (Linux)

### Translation Fails
- Check Google Cloud credentials are set correctly
- For African languages, ensure Spitch API key is set

### TTS Fails
- Check ElevenLabs API key is set
- For African languages, ensure Spitch API key is set

### Audio Separation Fails
- Ensure Demucs dependencies are installed
- Check that audio file is in supported format

## Adding New Languages

1. Create language directory: `v2/languages/{lang_code}/`
2. Create `__init__.py` and `language.py` files
3. Optionally add custom processors:
   - `transcription.py` for custom transcription
   - `translation.py` for custom translation
   - `tts.py` for custom TTS

Example:
```python
# v2/languages/de/language.py
DISPLAY_NAME = "German"
LANGUAGE_CODE = "de"
USE_WHISPER = True
USE_GOOGLE_TRANSLATE = True
USE_ELEVENLABS = True
```

