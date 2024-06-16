from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

model_name = 'distilgpt2'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
generator = pipeline('text-generation', model=model, tokenizer=tokenizer)

def format_text(text):
    text = text.replace('\n', ' ').replace('\n\n', ' ').strip()
    return text

def generate_post(context_words, platform):
    if platform.lower() == 'twitter':
        max_length = 50  # Researched twitters limit
    elif platform.lower() == 'instagram':
        max_length = 200  # checked instagrams limit too
    else:
        max_length = 100  # default length for other platforms

    prompt = " ".join(context_words)

    generated = generator(prompt, max_length=max_length, num_return_sequences=1)
    generated_text = generated[0]['generated_text']

    cleaned_text = format_text(generated_text)

    hashtags = ' '.join([f'#{word}' for word in context_words])
    generated_text_with_hashtags = f"{cleaned_text} {hashtags}"

    return generated_text_with_hashtags

if __name__ == "__main__":
    context_words = ["summer", "vacation", "beach"]
    platform = "Twitter"
    print(generate_post(context_words, platform))
