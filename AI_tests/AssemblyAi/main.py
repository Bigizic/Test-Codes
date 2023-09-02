#!/usr/bin/python3
""" """

import requests
import json
import time
from sys import argv

def ai_transcript():
    api_key = input("Enter api key: ")
    local_file = input("Are you uploading from local computer or\
            a url?\n If Local file enter 1 else enter 2")

    base_url = "https://api.assemblyai.com/v2"

    header = {
            "authorization": argv[1]
    }

    # Upload your local file to the AssemblyAi APi
    """
    with open(argv[2], "rb") as open_file:
        response = requests.post(base_url + "/upload",
                                 headers = header,
                                 data = open_file)
    """

ai_transcript()
