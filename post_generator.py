from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

def generate_post(context_words, platform):
    model_name = 'gpt2'

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    generator = pipeline('text-generation', model=model, tokenizer=tokenizer)

    if platform.lower() == 'twitter':
        max_length = 50  # Researched twitters limit
    elif platform.lower() == 'instagram':
        max_length = 200  # checked instagrams limit too
    else:
        max_length = 100

    prompt = " ".join(context_words)

    generated = generator(prompt, max_length=max_length, num_return_sequences=1)

    return generated[0]['generated_text']

if __name__ == "__main__":
    context_words = ["summer", "vacation", "beach"]
    platform = "Twitter"
    print(generate_post(context_words, platform))
