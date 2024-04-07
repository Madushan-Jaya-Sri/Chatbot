from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


gemini_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=AIzaSyA7iJsRW3iyXBFIu8Dt9C-E8Uy_e56FNUM'
# Replace 'YOUR_API_KEY_HERE' with your actual API key

# Function to send requests to the Gemini API
def send_gemini_request(prompt):
    import time
    import requests
    
    # Define headers
    headers = {'Content-Type': 'application/json'}
    
    # Define the request payload
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    # Send POST request with retry mechanism
    retry_count = 0
    while retry_count < 3:  # Retry for a maximum of 3 times
        try:
            # Send the request to the Gemini API
            response = requests.post(gemini_url, json=payload, headers=headers)
            response_json = response.json()
            if 'error' in response_json:
                return None
            else:
                return response_json
        except Exception as e:
            retry_count += 1
            time.sleep(2 ** retry_count)  # Exponential backoff

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

# Route for home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for chat response
@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.json
    user_input = data.get('user_input')
    response = generate_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
