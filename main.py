import asyncio
from binance.client import Client
from telebot import TeleBot
from telebot.types import Message
from init_config import initial_config
from mon_vol import monitor_vol

bot = TeleBot(initial_config("bot_token"))
api_key = initial_config("binance_api_key")
api_secret = initial_config("binannce_api_secret")
client = Client(api_key, api_secret)
all_tasks = {}
loop = asyncio.new_event_loop()

# Define a function to monitor the coin's volume
@bot.message_handler(commands=['monvol'])
def set_monitor_vol(message: Message):
    chat_id = message.chat.id
    name = f"{message.from_user.first_name} {message.from_user.last_name}"
    coin = message.text.split()[1].upper()
    symbol = coin + 'USDT'
    # Check if the event loop is already running
    task = loop.create_task(monitor_vol(chat_id, symbol, bot, client))
    all_tasks[(chat_id, symbol)] = task
    print(f"Bot started monitoring {symbol} for chat_id: {name}")
    bot.send_message(chat_id, f"Бот начал мониторинг {symbol}")
    try:
        loop.run_forever()
    except:
        pass

@bot.message_handler(commands=['stopmon'])
def stop_mon_coin(message: Message):
    chat_id = message.chat.id
    name = f"{message.from_user.first_name} {message.from_user.last_name}"
    coin = message.text.split()[1].upper()
    symbol = coin + 'USDT'
    task = all_tasks.get((chat_id, symbol))
    if task:
        task.cancel()
        all_tasks.pop((chat_id, symbol))
        print(f"Stopped monitoring {symbol} for : {name}")
    else:
        bot.reply_to(message, f"No monitoring task found for {symbol}")

if __name__ == '__main__':
    print("Bot starting!")
    bot.polling(none_stop=True)
    asyncio.set_event_loop(loop)