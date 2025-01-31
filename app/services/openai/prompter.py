from openai import OpenAI

client = OpenAI()

new_character = client.chat.completion.create(
    model="gpt-4o-mini",
    messages=[{"role": "developer", "content": ""}, {"role": "user", "content": ""}],
)
