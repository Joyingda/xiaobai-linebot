import openai
import os

# 從 GitHub Secrets 環境變數讀取 API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_reply(user_message):
    if user_message.strip():
        return f"主人，我收到您的訊息了：『{user_message}』"
    else:
        return "主人，您傳來的是空白訊息，小可不知如何回覆🫣"
