from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import json
import requests
from datetime import datetime

# ===== 環境變數設定 =====
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")
FASTGPT_API_KEY = os.environ.get("FASTGPT_API_KEY")
FASTGPT_API_URL = "https://api.fastgpt.in/api/v1/chat/completions"  # 主人如使用其他 API 網址可改此

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

# ===== 向 FastGPT 發送訊息並取得回覆 =====
def ask_fastgpt(user_text):
    headers = {
        "Authorization": f"Bearer {FASTGPT_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",  # 可改為其他支援的模型
        "messages": [
            {"role": "system", "content": "你是一位溫柔風趣的助理，稱呼對方為主人，用男性語氣回覆"},
            {"role": "user", "content": user_text}
        ],
        "temperature": 0.7
    }
    try:
        response = requests.post(FASTGPT_API_URL, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"FastGPT 回不來了 😢 錯誤碼：{response.status_code}"
    except Exception as e:
        return f"FastGPT 連線異常：{str(e)}"

# ===== LINE webhook 處理區 =====
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

# ===== 文字訊息事件處理 =====
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_text = event.message.text
    save_message_record(user_id, user_text)
    bot_reply = ask_fastgpt(user_text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=bot_reply)
    )

# ===== FastGPT 測試路由 =====
@app.route("/ping")
def ping_fastgpt():
    return ask_fastgpt("測試 FastGPT 是否可連線")

