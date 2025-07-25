import openai

openai.api_key = "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"  # 🔥直接在這裡填入金鑰

def generate_reply(user_message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一個友善、理解上下文的LINE聊天機器人"},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7
    )
    return response["choices"][0]["message"]["content"]
