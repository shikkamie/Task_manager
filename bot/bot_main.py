import os
import vk_api
import random
from dotenv import load_dotenv
from vk_api.bot_longpoll import VkBotLongPoll

load_dotenv()
group_id = 78483579
class Bot:
    def __init__(self, group_id, token):
        self.group_id = group_id
        self.token = token

        try:
            self.vk = vk_api.VkApi(token=token)
            self.long_poller = VkBotLongPoll(self.vk, self.group_id)
            self.api = self.vk.get_api()

        except vk_api.ApiError as auth_error:
            print(f"auth_error{auth_error}")
        except Exception as e:
            print(f"error{e}")

    def run(self):
        for event in self.long_poller.listen():
            try:
                print("Получено событие")
                self.on_event(event)
            except Exception as e:
                print(f"error{e}")

    def on_event(self, event):
        if event.type != vk_api.bot_longpoll.VkBotEventType.MESSAGE_NEW:
            print(f"Мы пока не умеем обрабатывать другие события {event.type}")


        else:
            self.api.messages.send(
                message=event.object.message['text'],
                random_id=random.randint(0, 2 ** 20),
                peer_id=event.object.message['peer_id']
            )



if __name__ == '__main__':
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("Token not found")
    else:
        bot = Bot(group_id, token= os.getenv("BOT_TOKEN"))
        bot.run()