from configure.configure import token_telegram
from datetime import date
import requests
from configure.configure import channel_id


class TelegramBot:
    """Class for message in status system"""

    @classmethod
    def send_telegram(cls, text: str):
        token = token_telegram
        url = "https://api.telegram.org/bot"
        url += token
        method = url + "/sendMessage"

        r = requests.post(method, data={
            "chat_id": channel_id,
            "text": text
        })

        if r.status_code != 200:
            raise Exception("post_text error")

    @classmethod
    def send_status_start(cls):
        cls.send_telegram(f"{date.today()}\nStatus: START")

    @classmethod
    def send_status_200(cls):
        cls.send_telegram(f"{date.today()}\nStatus: DONE")

    @classmethod
    def send_status_billding(cls):
        cls.send_telegram(f"{date.today()}\nStatus: ANALYSIS DONE")

    @classmethod
    def send_status_billding_400(cls):
        cls.send_telegram(f"{date.today()}\nStatus: ANALYSIS FAILED")

    @classmethod
    def send_status_400(cls):
        cls.send_telegram(f"{date.today()}\nStatus: FAILED")

