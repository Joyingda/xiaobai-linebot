from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import json
import requests
from datetime import datetime

# ===== 環境變數讀取區 =====
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = os.environ.get("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")  # 可改預設值

app = Flask(__name__)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ===== 儲存訊息紀錄 =====
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

# ===== 向 DeepSeek 發送請求 =====
def ask_deepseek(user_text):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    model_name = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
    temperature = float(os.environ.get("DEEPSEEK_TEMPERATURE", "0.7"))
    system_prompt = os.environ.get("DEEPSEEK_SYSTEM_PROMPT", "你是一位親切幽默的男僕助理，稱呼使用者為主人")
    data = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ],
        "temperature": temperature
    }
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"DeepSeek 回不來了 😢 錯誤碼：{response.status_code}"
    except Exception as e:
        return f"DeepSeek 連線異常：{str(e)}"

# ===== LINE webhook 路由 =====
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

# ===== 處理文字訊息 =====
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_text = event.message.text
    save_message_record(user_id, user_text)
    bot_reply = ask_deepseek(user_text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=bot_reply)
    )

# ===== DeepSeek 測試路由 =====
@app.route("/ping")
def ping_deepseek():
    return ask_deepseek("測試 DeepSeek 是否可連線")
