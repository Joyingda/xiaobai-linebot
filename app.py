from flask import Flask, request
from linebot.v3.messaging import MessagingApi, Configuration, ApiClient, ReplyMessageRequest, TextMessage, ApiException
from linebot.v3.webhook import WebhookParser
from linebot.v3.webhooks.models import MessageEvent, TextMessageContent
from linebot.v3.exceptions import InvalidSignatureError
import os
import openai

app = Flask(__name__)

# 環境變數讀取
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
channel_secret = os.getenv("LINE_CHANNEL_SECRET")
openai.api_key = os.getenv("OPENAI_API_KEY")

# LINE SDK 初始化
configuration = Configuration(access_token=channel_access_token)
api_client = ApiClient(configuration)
messaging_api = MessagingApi(api_client)
parser = WebhookParser(channel_secret)

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

            # GPT 回覆邏輯（小助理語氣設定）
            try:
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "你是一位溫柔、聰明又有條理的小助理，名字叫小白，"
                                "你在 LINE 上幫助主人處理日常大小事，回覆要簡潔、親切、聽話，"
                                "語氣要有輕快口吻，常使用『主人』稱呼對方，要自然不造作。"
                            )
                        },
                        {
                            "role": "user",
                            "content": user_text
                        }
                    ]
                )
                reply_text = completion.choices[0].message.content
            except Exception as e:
                reply_text = f"主人～小白暫時處理不了這條訊息呢，錯誤訊息如下：{str(e)}"

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
