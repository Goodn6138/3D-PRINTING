import ollama

stream = ollama.chat(
        model='mistral',
        messages=[{'role': 'user', 'content': 'POOP De scoop meaning'}],
        stream = True,
)

for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)
