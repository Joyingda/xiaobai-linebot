from flask import Flask, request
from linebot.v3.messaging import MessagingApi, ReplyMessageRequest, TextMessage, ApiException
from linebot.v3.webhook import WebhookParser
from linebot.v3.webhooks.models import MessageEvent, TextMessageContent
from linebot.v3.exceptions import InvalidSignatureError
from chatgpt_reply import get_reply
import os

app = Flask(__name__)

# 初始化 LINE Bot SDK
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
channel_secret = os.getenv("LINE_CHANNEL_SECRET")
messaging_api = MessagingApi(channel_access_token)
parser = WebhookParser(channel_secret)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        return "Invalid signature", 400

    for event in events:
        if isinstance(event, MessageEvent) and isinstance(event.message, TextMessageContent):
            user_text = event.message.text
            reply_text = get_reply(user_text)

            reply = ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_text)]
            )

            try:
                messaging_api.reply_message(reply)
            except ApiException as e:
                print(f"LINE API 回覆錯誤：{e.status} - {e.reason}")

    return "OK"
