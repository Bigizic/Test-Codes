#!/usr/bin/python3
""" """

import requests
import json
import time
from sys import argv

def ai_transcript():
    api_key = input("Enter api key: ")
    question = "Enter 1 to import from local file\n"
    file_type = input(question + "Enter 2 to import from url: ")

    base_url = "https://api.assemblyai.com/v2"

    header = {
            "authorization": api_key
    }

    # Upload your local file to the AssemblyAi APi
    if file_type == '1':
        file_path = input("Enter path to file: ")
        with open(file_path, "rb") as open_file:
            response = requests.post(base_url + "/upload",
                                     headers = header,
                                     data = open_file)
        upload_url = response.json()["upload_url"]
    if file_type == '2':
        file_url = input("Enter url: ")
        upload_url = file_url
    # use the upload_url returned by assemblyai api to create a
    # JSON payload containing the audio_url parameter
    data = {
        "audio_url": upload_url
    }
    # make post request to the assemblyai api endpoint with the
    # payload and headers

    url = base_url + "/transcript"
    response = requests.post(url, json=data, headers=header)

    transaction_id = response.json()['id']
    polling_endpoint = "https://api.assemblyai.com/v2/transcript/{}"\
                       .format(transaction_id)
    while True:
        transcription_result = requests.get(polling_endpoint, headers=header).json()
        if transcription_result['status'] == 'completed':
            print(transcription_result['text'])
            break;
        elif transcription_result['status'] == 'error':
            raise RuntimeError(f"Transcription failed: {transcription_result['error']}")
        else:
            time.sleep(3)


if __name__ == '__main__':
    ai_transcript()
