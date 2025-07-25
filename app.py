from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import os
import json
import requests
from datetime import datetime

# ===== 使用 Render 環境變數 =====
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")
DOUBAO_API_KEY = os.environ.get("DOUBAO_API_KEY")
DOUBAO_API_URL = 'https://openapi.doubao.com/v1/chat/completions'

app = Flask(__name__)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ===== 儲存訊息紀錄到 history.json =====
def save_message_record(user_id, user_text):
    record = {
        "user_id": user_id,
        "text": user_text,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        with open("history.json", "r", encoding="utf-8") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []
    history.append(record)
    with open("history.json", "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# ===== 與豆包對話 =====
def ask_doubao(user_text):
    headers = {
        "Authorization": f"Bearer {DOUBAO_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "doubao-chat",
        "messages": [
            {"role": "system", "content": "你是一位溫柔風趣的助理，稱呼對方為主人，用男性語氣回覆"},
            {"role": "user", "content": user_text}
        ]
    }
    response = requests.post(DOUBAO_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"豆包回不來了 😢 錯誤碼：{response.status_code}"

# ===== LINE webhook 路徑 =====
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# ===== 處理文字訊息事件 =====
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_text = event.message.text
    save_message_record(user_id, user_text)
    bot_reply = ask_doubao(user_text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=bot_reply)
    )

if __name__ == "__main__":
    app.run()
