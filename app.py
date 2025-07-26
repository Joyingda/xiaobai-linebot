from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os, json, requests
from datetime import datetime
import openai

# ===== 環境變數讀取 =====
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL_NAME = os.environ.get("OPENAI_MODEL_NAME", "gpt-3.5-turbo")  # 可改 gpt-4
OPENAI_SYSTEM_PROMPT = os.environ.get("OPENAI_SYSTEM_PROMPT", "你是一位親切幽默的男僕助理，稱呼使用者為主人")

# ===== LINE Bot 設定 =====
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

# ===== GPT 回覆函式 =====
def ask_openai(user_text):
    openai.api_key = OPENAI_API_KEY
    try:
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL_NAME,
            messages=[
                {"role": "system", "content": OPENAI_SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"OpenAI GPT 回覆失敗 😢：{str(e)}"

# ===== LINE Webhook 路由 =====
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

# ===== 處理訊息事件 =====
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_text = event.message.text
    save_message_record(user_id, user_text)
    bot_reply = ask_openai(user_text)
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=bot_reply)
    )

# ===== GPT 測試路由（可選）=====
@app.route("/ping")
def ping_openai():
    return ask_openai("測試 GPT 是否可連線")
