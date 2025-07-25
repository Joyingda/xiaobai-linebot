from flask import Flask, request
from linebot.v3.messaging import MessagingApi, Configuration, ApiClient, ReplyMessageRequest, TextMessage, ApiException
from linebot.v3.webhook import WebhookParser
from linebot.v3.webhooks.models import MessageEvent, TextMessageContent
from linebot.v3.exceptions import InvalidSignatureError
import os

app = Flask(__name__)

# 讀取環境變數
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
channel_secret = os.getenv("LINE_CHANNEL_SECRET")

# 使用 Configuration + ApiClient 初始化 MessagingApi ✅ 正確方式
configuration = Configuration(access_token=channel_access_token)
api_client = ApiClient(configuration)
messaging_api = MessagingApi(api_client)

# 初始化 webhook parser
parser = WebhookParser(channel_secret)

# webhook 路由
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        print("❌ Invalid signature")
        return "Invalid signature", 400

    for event in events:
        print(f"🛰️ 收到事件：{event}")

        if isinstance(event, MessageEvent) and isinstance(event.message, TextMessageContent):
            user_text = event.message.text
            print(f"💬 使用者訊息：{user_text}")

            if "早安" in user_text:
                reply_text = "早安主人～今天有小可陪伴 💙"
            else:
                reply_text = f"主人您說的是：{user_text}"

            reply = ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_text)]
            )

            try:
                messaging_api.reply_message(reply)
            except ApiException as e:
                print(f"❌ 回覆失敗！{e.status} - {e.reason}")

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
