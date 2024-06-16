from flask import Flask, request, jsonify
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

HUGGING_FACE_API_URL = "https://api-inference.huggingface.co/models/distilgpt2"
HUGGING_FACE_API_TOKEN = os.getenv('HUGGING_FACE_API_TOKEN')

headers = {
    "Authorization": f"Bearer {HUGGING_FACE_API_TOKEN}"
}


def clean_text(text):
    text = text.replace('\n', ' ').replace('\n\n', ' ').strip()
    return text


def generate_post(context_words, platform):
    # Adjust the post length based on the platform
    if platform.lower() == 'twitter':
        max_length = 50  # Researched twitters text limit
    elif platform.lower() == 'instagram':
        max_length = 200  # checked instagrams limit too
    else:
        max_length = 100

    prompt = " ".join(context_words)

    while True:
        response = requests.post(
            HUGGING_FACE_API_URL,
            headers=headers,
            json={
                "inputs": prompt,
                "parameters": {"max_length": max_length, "num_return_sequences": 1}
            }
        )

        if response.status_code == 200:
            break

        if response.status_code == 503 and 'estimated_time' in response.json():
            estimated_time = response.json()['estimated_time']
            print(f"Model is loading, retrying in {estimated_time} seconds...")
            time.sleep(estimated_time)
        else:
            raise Exception(f"Failed to generate text: {response.text}")

    generated = response.json()
    generated_text = generated[0]['generated_text']

    cleaned_text = clean_text(generated_text)

    hashtags = ' '.join([f'#{word}' for word in context_words])
    generated_text_with_hashtags = f"{cleaned_text} {hashtags}"

    return generated_text_with_hashtags


