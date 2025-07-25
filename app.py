from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from chatgpt_reply import generate_reply  # 🔁 引入回覆模組

app = Flask(__name__)
line_bot_api = LineBotApi("XAE8ktzcikRi7RVHd2CFeoac0AJTmBXDlg92IvgOrHb8LulUCvEvYsGEZ/xe/l1IPLS6SZ5gIgIwBnQdf7TEJc6XJcFSPgGvcHrU2H/UXYBnb2IbHSxYYNSA3DztPHUBmr3rCponiG7cfgsThkz9JwdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("75aaf6512771a9f69e1e28e45162e2bf")

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except Exception as e:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_msg = event.message.text
    print("👉 使用者傳來的訊息：", user_message)  # ← 這行是加的 log
    reply_text = generate_reply(user_msg)  # ✨取得 ChatGPT 回覆
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
