import telegram
from telegram.ext import Updater, MessageHandler, Filters
import configparser
import logging
from ChatGPT_HKBU import HKBU_ChatGPT

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Initialize the Telegram bot
    updater = Updater(token=config['TELEGRAM']['ACCESS_TOKEN'], use_context=True)
    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Initialize the ChatGPT instance
    global chatgpt
    chatgpt = HKBU_ChatGPT(config)

    # Register handler for ChatGPT responses
    chatgpt_handler = MessageHandler(Filters.text & (~Filters.command), equipped_chatgpt)
    dispatcher.add_handler(chatgpt_handler)

    updater.start_polling()
    updater.idle()

def equipped_chatgpt(update, context):
    global chatgpt
    reply_message = chatgpt.submit(update.message.text)
    
    logging.info("Update: " + str(update))
    logging.info("Context: " + str(context))
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

if __name__ == '__main__':
    main()