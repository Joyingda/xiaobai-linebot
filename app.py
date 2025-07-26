import os
import openai
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# 🔐 環境變數設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL_NAME = os.environ.get("OPENAI_MODEL_NAME", "gpt-3.5-turbo")
OPENAI_SYSTEM_PROMPT = os.environ.get("OPENAI_SYSTEM_PROMPT", "你是一位親切幽默的女僕助理，稱呼使用者為主人")

# 🚀 初始化 LINE Bot
app = Flask(__name__)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ✅ OpenAI API 設定
openai.api_key = OPENAI_API_KEY
openai.base_url = OPENAI_BASE_URL

# 📫 LINE Webhook 路由
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except Exception as e:
        print(f"❌ Webhook 錯誤：{e}")
        abort(400)
    return 'OK'

# 🤖 處理訊息事件
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_input = event.message.text

    # 📡 Debug 訊息
    print(f"📡 呼叫 GPT base_url：{openai.base_url}")
    print(f"🔧 模型使用：{OPENAI_MODEL_NAME}")
    print(f"💬 使用者輸入：{user_input}")

    try:
        response = openai.chat.completions.create(
            model=OPENAI_MODEL_NAME,
            messages=[
                {"role": "system", "content": OPENAI_SYSTEM_PROMPT},
                {"role": "user", "content": user_input},
            ]
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = f"❌ 錯誤：GPT 回覆失敗！{str(e)}"
        print(f"⚠️ GPT 錯誤：{e}")

    # 🗣️ 回覆使用者
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

# 🧪 本地開發啟動
if __name__ == "__main__":
    app.run()
