from flask import Flask, render_template, request, jsonify
import openai  # Changed import
import os
from dotenv import load_dotenv
import time

load_dotenv()

app = Flask(__name__)

# Configure OpenAI with Azure settings
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")  # Add this line

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        conversation_history = data.get('history', [])
        
        # Prepare messages for the conversation
        messages = conversation_history + [
            {"role": "user", "content": user_message}
        ]
        
        # Make API call to Azure OpenAI
        response = openai.ChatCompletion.create(
            engine=DEPLOYMENT_NAME,
            messages=messages,
            temperature=0.7,
            max_tokens=800
        )
        
        # Extract the assistant's response
        assistant_message = response.choices[0].message['content']
        
        return jsonify({
            'response': assistant_message,
            'history': messages + [{"role": "assistant", "content": assistant_message}]
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")  # Add this for debugging
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)