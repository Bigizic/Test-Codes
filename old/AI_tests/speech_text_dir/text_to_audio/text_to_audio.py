#!/usr/bin/python3
""" """

import requests


def text_to_audio():
    url = "https://play.ht/api/v2/tts"
    api = input("Enter api-key: ")
    content = input("Enter text: ")
    voice = input("Choose voice: ")

    playload = {
        "content": [content],
        "voice": voice
    }
    header = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    response = requests.post(url, json=payload, headers=header)
    if response.status_code >= 201:
        print("Error: {}".format(response.status_code))
        return

    print(response.text)


if __name__ == '__main__':
    text_to_audio()
