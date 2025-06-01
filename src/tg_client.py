import random
import threading
from urllib.parse import urlparse, parse_qs

from telegram.client import Telegram


class TgClient:
    def __init__(self, phone, api_id=27107768, api_hash="18b0bf93dbf4d97d72024ca8ff40f66a"):
        self.tg = Telegram(
            api_id=api_id,
            api_hash=api_hash,
            phone=phone,  # you can pass 'bot_token' instead
            database_encryption_key='',
            files_directory='_temp/',
            library_path="src/tdlib/tdjson.dll",
            login=True
        )
        self.tg.get_chats(limit=500).wait()

        r = self.tg.get_me()
        r.wait()
        self.is_premium = r.update["is_premium"]
        self.slots_id = None

        if self.is_premium:
            self.slots_id = self.get_boost_slots_id()

    def get_boost_slots_id(self):
        r = self.tg.call_method("getAvailableChatBoostSlots")
        r.wait()
        slots = r.update["slots"]
        return [s["slot_id"] for s in slots]

    def boost_chat(self, chat_id):
        # search_result = self.tg.call_method("searchPublicChat", params={"username": username})
        # search_result.wait()
        # chat_id = search_result.update['id']

        slot_ids = [random.choice(self.slots_id)]
        r = self.tg.call_method("boostChat", {
            "chat_id": chat_id,
            "slot_ids": slot_ids
        })
        r.wait()
        if r.error:
            raise Exception(r.error_info)

    def join_channel(self, username):
        search_result = self.tg.call_method("searchPublicChat", params={"username": username})
        search_result.wait()
        if search_result.error:
            raise Exception(search_result.error_info)

        chat_id = search_result.update["id"]
        r = self.tg.call_method("joinChat", {"chat_id": chat_id})
        r.wait()
        if r.error:
            raise Exception(r.error_info)
        return chat_id

    def get_web_app_init_data(self):
        search_result = self.tg.call_method("searchPublicChat", params={"username": "mrkt"})
        search_result.wait()

        r = self.tg.call_method('openWebApp', params={
            "chat_id": 8156315866,
            "bot_user_id": 8156315866,
            "url": "https://t.me/mrkt/app",
            "message_thread_id": 0,
            "reply_to": None,
            "parameters": {
                "@type": "webAppOpenParameters",
                "theme": None,
                "application_name": "app",
                "mode": None
            }
        })
        r.wait()
        url = r.update['url']
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.fragment)
        return query_params["tgWebAppData"][0]

    def get_available_gifts(self) -> list[dict]:
        m = self.tg.call_method("getAvailableGifts")
        m.wait()

        return m.update["gifts"]

    def send_message(self, chat_id, text):
        send_message_result = self.tg.send_message(
            chat_id=chat_id,
            text=text,
        )
        send_message_result.wait()

        if send_message_result.error:
            print(f"Failed to send the message: {send_message_result.error_info}")

        message_has_been_sent = threading.Event()

        def update_message_send_succeeded_handler(update):
            print(f"Received updateMessageSendSucceeded: {update}")
            # When we sent the message, it got a temporary id. The server assigns permanent id to the message
            # when it receives it, and tdlib sends the updateMessageSendSucceeded event with the new id.
            #
            # Check that this event is for the message we sent.
            if update["old_message_id"] == send_message_result.update["id"]:
                new_message_id = update["message"]["id"]
                print(f"Message has been sent. New message id: {new_message_id}")
                message_has_been_sent.set()

            # When the event is received, the handler is called.

        self.tg.add_update_handler("updateMessageSendSucceeded", update_message_send_succeeded_handler)

        # Wait for the message to be sent
        message_has_been_sent.wait(timeout=60)
        print("Message has been sent.")
