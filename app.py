from flask import Flask, request, jsonify
from post_generator import generate_post
from flask_cors import CORS,cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/', methods=['POST'])
@cross_origin(supports_credentials=True)
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
    port = 5000
    app.run(debug=False, host='0.0.0.0', port=port)