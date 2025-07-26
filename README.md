# 🤖 Xiaobai LINE Bot

使用 Python、Flask、LINE Messaging API 與 GPT API 打造的親切男僕 AI 聊天機器人！

## 🚀 功能特色

- 💬 LINE 官方帳號訊息互動
- 🧠 GPT 模型回應（gpt-3.5-turbo 為預設）
- 🌐 公益 GPT API `https://free.v36.cm` 支援
- 🔧 Render 平台自動部署
- 📝 支援自訂系統提示語與模型名稱

## 🔑 Render 環境變數

| 變數名稱             | 說明                                   |
|----------------------|----------------------------------------|
| LINE_CHANNEL_ACCESS_TOKEN | LINE Bot 的 Access Token |
| LINE_CHANNEL_SECRET       | LINE Bot 的 Channel Secret |
| OPENAI_API_KEY            | GPT API 金鑰（來自 v36 平台） |
| OPENAI_BASE_URL           | GPT API 基底網址（如 `https://free.v36.cm/v1`） |
| OPENAI_MODEL_NAME         | 使用模型名稱（如 `gpt-3.5-turbo`） |
| OPENAI_SYSTEM_PROMPT      | 指令語氣（如：「你是一位親切幽默的男僕助理，稱呼使用者為主人」） |

## ▶️ 啟動方式

```bash
gunicorn app:app
