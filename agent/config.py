import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

GITLAB_URL = os.getenv("GITLAB_URL", "https://gitlab.com")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
GITLAB_PROJECT_ID = os.getenv("GITLAB_PROJECT_ID")
GITLAB_REF = os.getenv("GITLAB_REF", "main")

GITLAB_TRIGGER_TOKEN = os.getenv("GITLAB_TRIGGER_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is missing")

if not GITLAB_TOKEN:
    raise ValueError("GITLAB_TOKEN is missing")

if not GITLAB_TRIGGER_TOKEN:
    raise ValueError("GITLAB_TRIGGER_TOKEN is missing")

if not GITLAB_PROJECT_ID:
    raise ValueError("GITLAB_PROJECT_ID is missing")