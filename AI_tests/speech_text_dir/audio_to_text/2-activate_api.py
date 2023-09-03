#!/usr/bin/python

# `pip3 install assemblyai` (macOS)
# `pip install assemblyai` (Windows)

import assemblyai as aai

aai.settings.api_key = "4cca1ea6a87c477b87a5372cf5c69e2a"
transcriber = aai.Transcriber()

transcript = transcriber.transcribe("https://storage.googleapis.com/aai-web-samples/news.mp4")
# transcript = transcriber.transcribe("./my-local-audio-file.wav")

print(transcript.text)
