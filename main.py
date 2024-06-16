from flask import Flask, request, jsonify
from post_generator import generate_post

app = Flask(__name__)

@app.route('/', methods=['POST'])
def generate():
    data = request.json
    context_words = data.get('context_words', [])
    platform = data.get('platform', 'Generic')

    post = generate_post(context_words, platform)
    return jsonify({"post": post})


if __name__ == '__main__':
    app.run(debug=True)
