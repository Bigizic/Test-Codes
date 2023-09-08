#!/usr/bin/python

import assemblyai as aai
from sys import argv

# Set your API key here
api_key = argv[1]

# Initialize the AssemblyAI client
client = aai.Client(api_key)

# URL of the YouTube video you want to transcribe
video_url = argv[2]

# Create a transcription job
job = client.transcribe_url(video_url)

# Wait for the job to complete
job.wait_for_completion()

# Get the transcription result
transcript = job.get_transcript()

# Print the transcription text
print(transcript.text)

