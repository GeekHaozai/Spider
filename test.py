import requests
import json

# https://ai.google.dev/tutorials/python_quickstart
def gemini(question):
    headers = {
        'Content-Type': 'application/json',
    }
    params = {'key':'AIzaSyBTEwaRhEP8icZSU2MPEDmBP1kXhSKJgWY'}
    data_dic = {"contents":{"parts":{"text":question}}}
    data = json.dumps(data_dic)
    response = requests.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent', headers=headers, params=params, data=data)
    print(response.text)
gemini("你是文心一言吗")