#!/usr/bin/python3
"""my first attempt on fiddling and scrapping data from data.gov
"""
import requests

api_url = "http://api.census.gov/data/2021/pep/population"
response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    new_data = {}
    for key, value in data.items():
        if key == 'describedBy':
            new_data[key] = value
        elif key == 'dataset':
            new_data[key] = value
    print(new_data)
