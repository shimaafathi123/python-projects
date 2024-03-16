from flask import Flask, render_template, request, jsonify
import nltk
from nltk.chat.util import Chat, reflections

app = Flask(__name__)

patterns = [
    (r'hi|hello|hey there', ['Hello!', 'Hi there!', 'Hey!']),
    (r'how are you?', ['I am doing well, thank you!', 'I\'m good, thanks for asking.']),
    (r'what\'s your name?', ['You can call me Chatbot.', 'I\'m Chatbot!']),
    (r'quit|exit', ['Goodbye!', 'Bye!', 'Take care!']),
]

default_response = ['I\'m not sure what you mean.', 'Could you please rephrase that?']

chatbot = Chat(patterns, reflections)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    response = chatbot.respond(user_input)
    if not response:
        response = default_response
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
