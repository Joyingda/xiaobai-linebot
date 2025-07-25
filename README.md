# xiaobai-linebot 🤖

使用 LINE Bot SDK + Flask + OpenAI API 的智慧回覆機器人 ✨  
金鑰皆使用 GitHub Secrets 或 Render 環境變數儲存，安全可靠 🔐

## 安裝需求
- Python 3.x
- Flask
- LINE Bot SDK
- OpenAI SDK

## 環境變數（設定於 Render 或 GitHub Secrets）
| 變數名稱 | 說明 |
|----------|------|
| OPENAI_API_KEY | OpenAI 的 API 金鑰 |
| LINE_CHANNEL_SECRET | LINE Developers 中的 Secret |
| LINE_CHANNEL_ACCESS_TOKEN | LINE Bot 的 Access Token |

## 部署方式
1. 建立 Render Web Service，選擇 Python
2. 上傳專案並設定 `render.yaml`
3. 設定 Webhook URL 至 LINE Bot 後台
4. 測試訊息回覆！

## 聯絡小可
如果您看到這行，就代表主人完成了 LINE Bot 的重生任務 ✨🎩
