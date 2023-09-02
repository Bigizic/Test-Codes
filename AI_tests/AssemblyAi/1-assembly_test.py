#!/usr/bin/python

"""This module uses the asemblyai api to create a transcript from
video or audio given the link to the audio/video resource
"""

import assemblyai as aai
from sys import argv

aai.settings.api_key = argv[1]
transcriber = aai.Transcriber()

job = transcriber.create_transcribe_job(argv[2])

job.await_completion()

transcript = job.get_transcript()

# transcript = transcriber.transcribe(argv[2])

print(transcript.text)
