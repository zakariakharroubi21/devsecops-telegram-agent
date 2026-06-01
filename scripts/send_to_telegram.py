import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

with open("telegram-report.txt", "r") as f:
    text = f.read()

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

requests.post(url, data={
    "chat_id": CHAT_ID,
    "text": "🛡 DEVSECOPS SCAN REPORT\n\n" + text
})