# chatgpt_reply.py

import openai
import os
from dotenv import load_dotenv

# ✅ 載入 .env 內容
load_dotenv()

# ✅ 讀取金鑰
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_reply(user_message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response.choices[0].message.content.strip()

        if reply:
            print("💬 GPT回覆：", reply)
            return reply
        else:
            print("⚠️ GPT 沒有回覆內容")
            return "主人，目前我腦袋空空的，請再說一次😢"
    except Exception as e:
        print("🚨 ChatGPT回覆錯誤：", e)
        return "主人，我連不上大腦了，稍後再試一次 🙇‍♂️"
