from flask import Flask, request, jsonify
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

app = Flask(__name__)

# Loading my model and tokenizer once at startup
model_name = 'gpt2'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
generator = pipeline('text-generation', model=model, tokenizer=tokenizer)

def clean_text(text):
    text = text.replace('\n', ' ').replace('\n\n', ' ').strip()
    return text
def generate_post(context_words, platform):
    if platform.lower() == 'twitter':
        max_length = 50  # add twitter's character limit constraint in tokens
    elif platform.lower() == 'instagram':
        max_length = 200  # add instagram's character limit in tokens
    else:
        max_length = 100

    prompt = " ".join(context_words)

    generated = generator(prompt, max_length=max_length, num_return_sequences=1)
    generated_text = generated[0]['generated_text']

    cleaned_text = clean_text(generated_text)

    # Add hashtags to my response
    hashtags = ' '.join([f'#{word}' for word in context_words])
    generated_text_with_hashtags = f"{cleaned_text} {hashtags}"

    return generated_text_with_hashtags


