
api_key = "AIzaSyA7iJsRW3iyXBFIu8Dt9C-E8Uy_e56FNUM"  # Replace with your actual key
import time
import requests

# Define the Gemini API endpoint URL and API key
gemini_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'
gemini_api_key = "AIzaSyA7iJsRW3iyXBFIu8Dt9C-E8Uy_e56FNUM"  # Replace with your actual Gemini API key

# Function to send requests to the Gemini API
def send_gemini_request(prompt):
    try:
        # Define headers
        headers = {'Content-Type': 'application/json'}
        
        # Define the request payload
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        
        # Send POST request with API key
        params = {'key': gemini_api_key}
        response = requests.post(gemini_url, json=payload, headers=headers, params=params)
        response_json = response.json()
        
        if 'error' in response_json:
            print(f"Error: {response_json['error']['message']}")
            return None
        else:
            return response_json
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

# Function to generate response from Gemini API
def generate_response(input_text):
    try:
        response_json = send_gemini_request(input_text)
        candidate = response_json['candidates'][0]
        parts = candidate['content']['parts'][0]['text']
        return parts
    except (KeyError, IndexError):
        return "Error: No response from Gemini API"

# Function to start the chatbot
def start_chatbot():
    print("Chatbot: Hello! I'm a chatbot powered by Gemini API. You can start chatting with me.")
    print("Chatbot: Type 'exit' to end the conversation.")
    
    while True:
        user_input = input("User: ")
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break
        
        response = generate_response(user_input)
        print("Chatbot:", response)

# Start the chatbot
start_chatbot()
