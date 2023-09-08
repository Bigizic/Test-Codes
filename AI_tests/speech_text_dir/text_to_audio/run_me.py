#!/usr/bin/python3
"""This module is like run_me_sample but it prompts the user for
a text to generate a voice of the text the user passed.
    You can save the audio file or download it if you like
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
    """function definition """
    api = input("Enter User ID: ")
    secret_key = input("Enter secret key: ")
    # check if api and secret_key is valid
    url = "https://play.ht/api/v2/tts"
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
    msg = "Do you want to use the default voice? (y/yes) or (n/no) "
    text = input("Enter Tex:  ")
    pro = input(msg)
    while True:
        pr = pro.lower()
        if pr not in ['no', 'n'] or pr not in ['yes', 'y']:
            pro = input("Enter y or n: ")
        else:
            break
    if pro.lower() == 'yes':
        msg = "Enter 1 to select default male voice"
        word = f'{msg} Enter 2 to select deafult female voice '
        gender = input(word)
        while True:
            if gender not in ['1', '2']:
                gender = input("Enter 1 for male, 2 for female: ")
            else:
                break
    if pro.lower() == 'no':
        msg = "Did you try the run_me_sample?? You can get a"
        print(f'{msg} voice sample to use if you do')
    voice = "larry" if gender == '1' else 
