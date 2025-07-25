# chatgpt_reply.py
import openai
import os

# ✅ 建議使用環境變數管理金鑰，較安全
openai.api_key = os.getenv("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")

def get_reply(user_message):
    try:
        # ✅ 呼叫 ChatGPT API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message.content.strip()

        # ✅ 判斷是否有回覆內容
        if reply:
            print("💬 GPT回覆：", reply)
            return reply
        else:
            print("⚠️ GPT 沒有回覆內容")
            return "主人，目前我腦袋空空的，請再說一次😢"
    except Exception as e:
        print("🚨 ChatGPT回覆錯誤：", e)
        return "主人，我連不上大腦了，稍後再試一次 🙇‍♂️"

