import requests
import os
from decouple import config


# Set your API key
api_key = config('CGPT_TOKEN')

# Set the endpoint URL
url = "https://api.openai.com/v1/chat/completions"

# Define the headers with the API key
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Define the data payload, including the model and the message
data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Can you tell me a joke?"}
    ],
    "max_tokens": 50
}

# Send the POST request to the API
response = requests.post(url, headers=headers, json=data)

# Check if the request was successful
if response.status_code == 200:
    response_data = response.json()
    message = response_data['choices'][0]['message']['content']
    print("ChatGPT Response:", message)
else:
    print(f"Request failed with status code {response.status_code}")
    print("Response:", response.text)
