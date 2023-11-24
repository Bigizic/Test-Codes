#!/usr/bin/python3
"""This module uses the play api to check the available voices
a user can generate and filter the data according to the user
prefences
"""

import requests
import language_checker


def final_language():
    """Formats the language from language_checker to `language (Cn)`
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
    #api = input("Enter User ID: ")
    #secret_key = input("Enter secret key: ")
    pref = " [1: Standard voice type], [2: Neural voice type]"
    gender = input("Enter gender: ")
    voice_type = input("Select voice type" + pref + ": ")
    # pref = "\n>>>\tEg. English, Turkish, Swedish"
    ok = "please try changing your query maybe the gender {}".format(
          "voice-type/langauage")
    lang = final_language()
    api = '91xSeuUNvCVUei2vwnHy0oh6j112'
    secret_key = '4d79ed39544f4a0897996cc0174d9e33'

    url = "https://play.ht/api/v1/getVoices"

    header = {
        "accept": "application/json",
        "AUTHORIZATION": secret_key,
        "X-USER-ID": api
    }
    if voice_type == '2':
        v = 'Neural'
    else:
        v = 'Standard'

    preferences = {
        "gender": gender,
        "voiceType": v,
        "language": lang
    }
    """g = "Female" if gender == 'Male' else "Male"
    sec_preferences = {
        "gender": g,
        "voiceType": v,
        "language": lang
    }"""
    try:
        response = requests.get(url, headers=header)
        response.raise_for_status()

        match_check = True
        json_format = response.json()
        if json_format and "voices" in json_format:
            match = []
            sample = []
            for voice in json_format["voices"]:
                is_match = all(voice.get(k) == v for k, v in
                               preferences.items())
                if is_match:
                    match_check = False
                    match.append(voice.get("name"))
                    sample.append(voice.get("sample"))
                if not is_match and not match_check:
                    match_check = True
            if match_check:
                print("Perfroming deep Search\n>>> You can change {}"
                        .format("the Gender or proceed with prev one"))
                q = input("Gender swap? Enter (y/yes) (n/no): ")
                if q == 'y' or q == 'yes':
                    g = input("lets try changing the gender, {}"
                              .format(f'you entered {gender} change it: '))
                elif q == 'n' or q == 'no':
                    g = gender
                sec_preferences = {
                    "gender": g,
                    "voiceType": v,
                    "language": lang
                }
                for voice in json_format["voices"]:
                    sec_match = all(voice.get(k) == v for k, v in
                                    sec_preferences.items())
                    if sec_match:
                        match.append(voice.get("name"))
                        sample.append(voice.get("sample"))
                    else:
                        print(ok)
                        return

        for items in match:
            print("Name of voices: {}".format(items))
        for items in sample:
            print("Listen to a sample here: {}".format(items))
            print()
    except ValueError:
        print("Nope not a valid json")


if __name__ == '__main__':
    voices()
