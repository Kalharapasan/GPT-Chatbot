import openai

openai.api_key ="my Api"

def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit','bye']:
            print("Exiting the chat. Goodbye!")
            break
        gpt_response = chat_with_gpt(user_input)
        print(f"GPT",gpt_response)
              