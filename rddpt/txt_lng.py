from openai import OpenAI

def translate_text(text, target_language):
    """
    translate text to the target language using OpenAI's GPT model.
    """
    client = OpenAI()
    
    print(f"translating text to {target_language}...")
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"you are a helpful assistant that translates text to {target_language}."},
            {"role": "user", "content": f"translate the following text to {target_language}:\n\n{text}"}
        ]
    )
    
    translated_text = response.choices[0].message.content.strip()
    print("translation successful!")
    return translated_text
