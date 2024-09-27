import requests
import time
import random
import json

# Define the API endpoint for the firewall
FIREWALL_API_URL = 'http://127.0.0.1:5000/api/submit'

# Define the payloads for different attack types


'''
def send_payload(payload):
    try:
        response = requests.post(FIREWALL_API_URL, json=payload)
        print(f"Sent payload: {payload}, Response: {response.json()}")
    except Exception as e:
        print(f"Error sending payload: {e}")

def simulate_attacks():
    while True:
        # Randomly select a payload from the list
        payload = random.choice(payloads)
        
        # Send the selected payload
        send_payload(payload)
        
        # Wait for a random time between 5 to 6 seconds
        time.sleep(random.uniform(10,11))'''

def load_payloads(file_path):
    """
    Load payloads from a specified JSON file.
    """
    with open(file_path, 'r') as file:
        payloads = json.load(file)
    return payloads

def simulate_attacks():
    """
    Simulate attacks by sending payloads to the firewall.
    """
    # Load the payloads from the JSON file
    payloads = load_payloads("payload.json")

    # Start sending the payloads in a loop
    while True:
        payload = random.choice(payloads)  # Pick a random payload from the list
        try:
            response = requests.post(FIREWALL_API_URL, json=payload)
            print(f"Sent payload: {json.dumps(payload)}\nResponse: {response.status_code}")
        except Exception as e:
            print(f"Failed to send payload: {e}")
        
        # Sleep for a random interval between 10 and 11 seconds
        time.sleep(random.randint(10, 11))

if __name__ == "__main__":
    simulate_attacks()

'''
while True:
    payload = random.choice(payloads)  # Pick a random payload from the list
    try:
        response = requests.post(FIREWALL_API_URL, json=payload)
        print(f"Sent payload: {json.dumps(payload)}\nResponse: {response.status_code}")
    except Exception as e:
        print(f"Failed to send payload: {e}")
    time.sleep(random.randint(10,11))  

if __name__ == "__main__":
    simulate_attacks()'''
