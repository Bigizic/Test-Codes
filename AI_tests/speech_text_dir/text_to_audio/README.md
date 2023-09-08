# This directory contains python scripts that turn texts to audio using the <a href="https://play.ht/">Play.ht</a> api

To run:

There are two modes you can try the sample mode that generates the link to the data you provided, so you can download or listen to the sample voice

## To try `no text to audio script` use `./run_me_sample.py`:

This means you'll not be providing a text or given a prompt to enter a text to convert to audio but you'll be listening to available voices based on the data
you provided.

- [X] You'd need to create an account on <a href="https://play.ht/"> Play{dot}ht</a> request a secret key use the user id when you get the user id prompt, do the same for the secret key.

- Enter a gender, only genders allowed are male and female

- Enter 1 to use `Standard` voiceType or 2 for `Neural` voiceType

- Enter a country or language, if country is not found you can enter
a language use `language` rather but some countries are available for the language prompt

- You'll get the name of your voice actor and a link to download the sample voice or play it if you like


## To try `text to audio script` use `./run_me.py`
