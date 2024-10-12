# # Import libraries
# import os
# from flask import Flask,request,jsonify,render_template
# from dotenv import load_dotenv
# from openai import OpenAI
# client = OpenAI()

# # Set up OpenAI API Key
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# # Set up Flask app
# app = Flask(__name__)

# # Set up Upload Folder for Flask
# app.config['UPLOAD_FOLDER'] = 'static'

# # Set up Flask Routes
# @app.route('/',methods=['GET','POST'])
# def main():
#     if request.method == 'POST':
#         language = request.form['language']
#         file = request.files['file']
#         if file:
#             # Load audio file
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
#             audio_file = open("static/"+file.filename, "rb")
#             transcript = client.audio.transcriptions.create(
#                 model="whisper-1", 
#                 file=audio_file,
#             )
#             response = client.completions.create(
#                 model="gpt-4o-mini",
#                 message = [{'role':'system','content':f'You will be provided with a sentance in english, your task is to translate it into {language}'},
#                            {'role':'user','content':transcript.text}],
#                 temperature=0,
#                 max_tokens=256,
#             )
#             return jsonify(response.choices[0].message.content)
#     return render_template('index.html')


# if __name__ == '__main__':
#     app.run(debug=True)


# # Import libraries
# import os
# from flask import Flask, request, jsonify, render_template
# from dotenv import load_dotenv
# from openai import OpenAI
# client = OpenAI()

# # Load environment variables
# load_dotenv()

# # Set up OpenAI API Key
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# # Set up Flask app
# app = Flask(__name__)

# # Set up Upload Folder for Flask
# app.config['UPLOAD_FOLDER'] = 'static'

# # Set up Flask Routes
# @app.route('/', methods=['GET', 'POST'])
# def main():
#     if request.method == 'POST':
#         language = request.form['language']
#         file = request.files['file']
#         if file:
#             # Load audio file
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#             file.save(file_path)
            
#             # Transcribe the audio file
#             with open(file_path, "rb") as audio_file:  # Ensure file is properly closed after usage
#                 transcript = client.audio.transcriptions.create(
#                     model="whisper-1", 
#                     file=audio_file,
#                     response_format="text",
#                 )

#             # Generate translation response
#             response = client.completions.create(  # Fixed the method call to use ChatCompletion
#                 model="gpt-4",  # Ensure this is a valid model you have access to
#                 messages=[
#                     {'role': 'system', 'content': f'You will be provided with a sentence in English; your task is to translate it into {language}'},
#                     {'role': 'user', 'content': transcript.text}  # Correctly access 'text' from transcript
#                 ],
#                 temperature=0,
#                 max_tokens=256,
#             )
#             return jsonify({'translation': response.choices[0].message.content})  # Wrap in a dict for clarity
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)
# Import libraries
import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import openai
from openai import OpenAI
client = OpenAI()

# Load environment variables
load_dotenv()

# Set up OpenAI API Key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Set up Flask app
app = Flask(__name__)

# Set up Upload Folder for Flask
app.config['UPLOAD_FOLDER'] = 'static'

# Set up Flask Routes
@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        language = request.form['language']
        file = request.files['file']
        if file:
            # Load audio file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            
            # Transcribe the audio file using the new method
            with open(file_path, "rb") as audio_file:
                transcript_response = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file,
                )

            # Generate translation response using ChatCompletion
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {'role': 'system', 'content': f'You will be provided with a sentence in English; your task is to translate it into {language}'},
                    {'role': 'user', 'content': transcript_response.text}  # Accessing 'text' from the transcript response
                ],
            )
            return jsonify({'translation': response.choices[0].message.content})  # Wrap in a dict for clarity
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)