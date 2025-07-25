from flask import Flask, request
from linebot.v3.messaging import MessagingApi, ReplyMessageRequest, TextMessage, ApiException
from linebot.v3.webhook import WebhookParser
from linebot.v3.webhooks.models import MessageEvent, TextMessageContent
from linebot.v3.exceptions import InvalidSignatureError
import os

app = Flask(__name__)

# 環境變數讀取
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
channel_secret = os.getenv("LINE_CHANNEL_SECRET")

# LINE SDK 初始化
messaging_api = MessagingApi(channel_access_token)
parser = WebhookParser(channel_secret)

# Webhook 路由
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        return "Invalid signature", 400

    for event in events:
        if isinstance(event, MessageEvent) and isinstance(event.message, TextMessageContent):
            user_text = event.message.text

            # 回覆邏輯（可改成串接 chatgpt_reply）
            reply = ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=f"主人您說的是：{user_text}")]
            )

            try:
                messaging_api.reply_message(reply)
            except ApiException as e:
                print(f"回覆失敗！{e.status} - {e.reason}")

    return "OK"

# Flask 主程式啟動段（必加，否則閃退）
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
