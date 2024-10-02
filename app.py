import nltk
import ssl
import logging
from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from dotenv import load_dotenv
import os
import re
import random

# Configure logging
logging.basicConfig(level=logging.INFO)

# Attempt to create an unverified HTTPS context for NLTK downloads
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Attempt to download NLTK data, but continue if it fails
try:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
except Exception as e:
    logging.warning(f"Failed to download NLTK data: {str(e)}")

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure OpenAI API
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Initialize NLTK components
lemmatizer = WordNetLemmatizer()
try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    logging.warning("NLTK stopwords not available. Using an empty set.")
    stop_words = set()

# Fallback tokenization function
def simple_tokenize(text):
    return re.findall(r'\w+', text.lower())

def preprocess_text(text):
    try:
        # Try using NLTK's word_tokenize
        tokens = word_tokenize(text.lower())
    except LookupError:
        # Fallback to simple tokenization if NLTK data is not available
        logging.warning("NLTK tokenization failed. Using simple tokenization.")
        tokens = simple_tokenize(text.lower())
    
    # Remove punctuation and stopwords, then lemmatize
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in string.punctuation and token not in stop_words]
    return set(tokens)

def calculate_similarity(prompt, user_guess):
    prompt_tokens = set(simple_tokenize(prompt.lower()))
    guess_tokens = set(simple_tokenize(user_guess.lower()))
    
    intersection = len(prompt_tokens.intersection(guess_tokens))
    union = len(prompt_tokens.union(guess_tokens))
    similarity = intersection / union if union > 0 else 0
    
    return similarity

@app.route('/generate_image', methods=['POST'])
def generate_image():
    prompt = request.json['prompt']
    try:
        logging.info(f"Generating image for prompt: {prompt}")
        response = client.images.generate(
            model="dall-e-2",
            prompt=prompt,
            size="512x512",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        logging.info(f"Image generated successfully: {image_url}")
        return jsonify({'image_url': image_url})
    except Exception as e:
        logging.error(f"Error generating image: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/submit_guess', methods=['POST'])
def submit_guess():
    original_prompt = request.json['original_prompt']
    user_guess = request.json['user_guess']
    
    try:
        similarity = calculate_similarity(original_prompt, user_guess)
        
        if similarity > 0.3:  # Lowered threshold
            result = "Correct!"
            points = 5
        elif similarity > 0.1:  # Lowered threshold
            result = "Close!"
            points = 2
        else:
            result = "Try again."
            points = 0
        
        return jsonify({
            'result': result,
            'points': points,
            'similarity': similarity,
            'original_prompt': original_prompt  # Add this line to return the original prompt
        })
    except Exception as e:
        logging.error(f"Error in submit_guess: {str(e)}")
        return jsonify({'error': 'An error occurred while processing your guess.'}), 500

@app.route('/')
def index():
    return render_template('index.html')

# Add this list of random prompts
random_prompts = [
    "A futuristic city skyline at sunset",
    "A whimsical treehouse in an enchanted forest",
    "A steampunk-inspired flying machine",
    "An underwater scene with bioluminescent creatures",
    "A cozy cabin in a snowy mountain landscape",
    "A bustling alien marketplace on a distant planet",
    "A magical library with floating books",
    "A cyberpunk street scene at night",
    "A serene zen garden with a koi pond",
    "A fantastical castle in the clouds"
]

@app.route('/get_random_prompt', methods=['GET'])
def get_random_prompt():
    return jsonify({'prompt': random.choice(random_prompts)})

if __name__ == '__main__':
    app.run(debug=True)
