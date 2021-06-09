#from multiprocessing import spawn
from logging import log
import os
import sys
import json
import time
import threading
import requests
#import multiprocessing
#from multiprocessing import Process
import datetime
sys.path.append('.')
from server.config import TELEGRAM_API_KEY
from server.logger import get_logger

logger = get_logger("telegram-main-process")

class TelegramBot():
    def __init__(self, apikey, commands, update_intervall=0.5, threads=3):
        self.update_intervall = update_intervall
        self.commands = commands
        self.ApiKey = apikey

    @staticmethod
    def get_messages(updates, last_timestamp):
        #logger.debug(f'getting messages')
        num_updates = len(updates["result"]) - 1
        messages = []
        if num_updates > 0 and num_updates < 5:
            for x in range(0,num_updates):

                i = num_updates - 1 - x
                
                #logger.debug(f'trying message num { num_updates - i }')
                text = updates["result"][num_updates - i ]["message"]["text"]
                chat_id = updates["result"][num_updates - i ]["message"]["chat"]["id"]
                timestamp_message = float(updates["result"][num_updates - i ]["message"]["date"])

                
                #print(timestamp_message  > last_timestamp)

                if timestamp_message > last_timestamp:

                    messages.append([text, chat_id])

                    last_timestamp = timestamp_message
                    #print(last_timestamp, timestamp_message)
                
                else:
                    pass
            #print(timestamp_message, last_timestamp)
            return messages, chat_id
            
        elif num_updates >=5:

            for x in range(0,5):

                i = 4 - x
                
                #logger.debug(f'trying message num { num_updates - i }')
                text = updates["result"][num_updates - i ]["message"]["text"]
                chat_id = updates["result"][num_updates - i ]["message"]["chat"]["id"]
                timestamp_message = float(updates["result"][num_updates - i ]["message"]["date"])

                
                #print(timestamp_message  > last_timestamp)

                if timestamp_message > last_timestamp:

                    messages.append([text, chat_id])

                    last_timestamp = timestamp_message
                    #print(last_timestamp, timestamp_message)
                
                else:
                    pass
            #print(timestamp_message, last_timestamp)
            return messages, chat_id
        else:
            return []

     
    def run(self):
        # needed um zu verhindern das random messages gesendet werden
        messages, last_timestamp = self.get_messages(self.get_updates(), 0)
        while True:

            updates = self.get_updates()
            messages, last_timestamp = self.get_messages(updates, last_timestamp)

            start = time.perf_counter()

            logger.info(len(messages))
            if len(messages) > 2:
                threads = []
                for message in messages:
                    threads.append(threading.Thread(target=self.process_message, args=[message[0], message[1]]))
                for thread in threads:
                    thread.start()
                for thread in threads:
                    thread.join()
            else:
                for message in messages:
                    self.process_message(message[0], message[1])

            time_needed = time.perf_counter() - start

            sleep_time = float(self.update_intervall) - time_needed

            if sleep_time > 0:

                time.sleep(sleep_time)
            

    def start_bot(self):
        try: 
            self.run()
        except KeyboardInterrupt:
            print("shutting down")
        except Exception as e:
            logger.error(f'an error {e} has ocured while running the bot')

    def get_updates(self):
        #logger.debug(f'getting response')
        response = requests.get(f'https://api.telegram.org/bot{self.ApiKey}/getUpdates')
        return json.loads(response.content.decode("utf8"))

    def process_message(self, message, chat_id):
        if message in self.commands:
            message()
        else:
            self.send_message(message, chat_id)

    def send_message(self, message, chat_id):
        print(message, chat_id)
        url = f'https://api.telegram.org/bot{self.ApiKey}/sendMessage?text={message}&chat_id?{chat_id}&parse_mode=Markdown'
        res = requests.post(url)

        if res.status_code != 200:
            logger.error(f'an error has ocured status code {res.status_code, res.text}')


if __name__ == '__main__':
    bot = TelegramBot(TELEGRAM_API_KEY, {})

    bot.start_bot()