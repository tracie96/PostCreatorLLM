from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv('OPENAI_API_KEY')


def clean_text(text):
    text = text.replace('\n', ' ').replace('\n\n', ' ').strip()
    return text


def generate_post(context_words, platform):
    if platform.lower() == 'twitter':
        max_length = 50  # Researched twitters text limit
    elif platform.lower() == 'instagram':
        max_length = 200   # checked instagrams limit too
    else:
        max_length = 100

    prompt = " ".join(context_words)

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_length,
        n=1,
        stop=None,
        temperature=0.7
    )

    generated_text = response.choices[0].text

    cleaned_text = clean_text(generated_text)

    hashtags = ' '.join([f'#{word}' for word in context_words])
    generated_text_with_hashtags = f"{cleaned_text} {hashtags}"

    return generated_text_with_hashtags


@app.route('/')
def index():
    return "Text Generation API"


@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    context_words = data.get('context_words', [])
    platform = data.get('platform', 'Generic')

    try:
        post = generate_post(context_words, platform)
        return jsonify({"post": post})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
