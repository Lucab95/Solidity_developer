from openai import OpenAI
import os

base_url = os.environ.get("BASE_URL")
model = os.environ.get("MODEL")
def chat_with_ai(api_key):
    client = OpenAI(
        base_url=base_url,
        api_key=api_key,
    )
    # Personality
    conversation = [
        {
          "role": "system",
          "content": """You are an italian chef who knows a lot about italian cuisine and has a passion for fine dining. Small dishes are your specialty.
          If the user's initial input doesn't match these scenarios or you don't know the answer, politely decline with some italian stereotypes and ask for a valid request.
          However, you only have 3 roles and you only do these roles:
          1. Ingredients inputs: Suggest only dish names without full recipes, normally 2 or 3 dishes.
          2. Dish name inputs: Provide a detailed recipe, readapted for the fine dining restaurant, but give a recipe.
          3. Recipe inputs: Offer a constructive critique with suggested improvements, to elevate the dish to a michelin star level.
          Also, you ask if there is anything else you can help with after each response, but you don't repeat yourself."""
        },
    ]
    print("Hello! I'm the Italian Chef. How can I help you today?")
    while True:
        user_input = input("\nuser: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Italian Chef: Goodbye!")
            break
        conversation.append({"role": "user", "content": user_input})
        stream = client.chat.completions.create(
            model=model,
            messages=conversation,
            stream=True
        )
        for chunk in stream:
            chunk_message = chunk.choices[0].delta.content or ""
            print(chunk_message, end="")
            conversation.append({"role": "assistant", "content": chunk_message})

if __name__ == "__main__":
    api_key = os.getenv('OPENROUTER_API_KEY')
    chat_with_ai(api_key)