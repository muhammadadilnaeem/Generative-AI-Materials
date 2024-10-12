import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import openai
from openai import OpenAI

# Load environment variables
load_dotenv()

# Set up OpenAI API Key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('demo.html')

@app.route('/generateimages/<prompt>')
def generate(prompt):
    print("prompt:", prompt)
    response = client.images.generate(prompt=prompt, n=2, size="256x256")
    
    # Extract URLs from the response
    image_urls = [image.url for image in response.data]
    
    # Return a JSON response with image URLs
    return jsonify(images=image_urls)  # Change this line to return JSON

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
