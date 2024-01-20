#!/usr/bin/python3
"""This module uses the play api to check the available voices
a user can generate and filter the data according to the user
prefences
"""

import requests
import language_checker


def final_language():
    """Formats the language from language_checker to
    `language (LanguageCode)`
    """
    temp = language_checker.lang_checker()
    try:
        if ' ' in temp:
            parts = temp.split(' ')
            mp = parts[0]
            tmp = ' '.join(parts[1:])
            language = f'{mp} ({tmp})'
        else:
            language = temp
        return language
    except TypeError as e:
        print(e)


def voices():
    api = input("Enter User ID: ")
    secret_key = input("Enter secret key: ")
    # check if api and secret_key is valid
    url = "https://play.ht/api/v1/getVoices"
    header = {
        "accept": "application/json",
        "AUTHORIZATION": secret_key,
        "X-USER-ID": api
    }
    try:
        response = requests.get(url, headers=header)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e)
        return

    pref = " [1: Standard voice type], [2: Neural voice type]"
    gender = input("Enter gender: ")
    while True:
        if gender not in ['male', 'Male', 'Female', 'female']:
            gender = input("Error: enter male or female >> ")
        else:
            break

    voice_type = input("Select voice type" + pref + ": ")
    while True:
        if voice_type not in ['1', '2']:
            voice_type = input("Error: enter 1 or 2 >> ")
        else:
            break

    ok = "please try changing your query maybe the gender {}".format(
          "voice-type/langauage")
    lang = final_language()

    v = "Neural" if voice_type == '2' else "Standard"
    if lang:
        preferences = {
            "gender": gender,
            "voiceType": v,
            "language": lang
        }
    else:
        return
    try:
        response = requests.get(url, headers=header)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e)
        return
    try:
        json_format = response.json()
        if json_format and "voices" in json_format:
            match = {}
            for voice in json_format["voices"]:
                if (voice["gender"].lower() == gender.lower() and
                        voice["voiceType"].lower() == v.lower() and
                        voice["language"].lower() == lang.lower()):
                    match["name"] = voice.get("name")
                    match["sample"] = voice.get("sample")
            if match:
                print("Your JSON Data.. Thanks to play.ht")
                for key, value in match.items():
                    print(key, value, sep=": ")
                    print()
            else:
                print(ok)

    except ValueError:
        print("Not a valid JSON")


if __name__ == '__main__':
    voices()
