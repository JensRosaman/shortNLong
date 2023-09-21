import requests
from tensorflow.python.keras.models import nest
import gymnasium as gym
from gymnasium import 
url = r"http://127.0.0.1:5000/start_game"
data = {}  # Replace with your data if needed

# Send the POST request
response = requests.post(url, json=data)

# Check the response
if response.status_code == 200:
    # Request was successful
    result = response.json()
    print(f'Game ID: {result["game_id"]}')
else:
    # Request failed
    print(f'Error: {response.status_code}')
    print(response.text)


