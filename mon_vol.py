import asyncio
from binance.client import Client
from telebot import TeleBot
from telebot.types import Message
from datetime import datetime

async def monitor_vol(chat_id, symbol, bot, client):
    try:
        while True:
            candles = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_15MINUTE, limit=2)
            prev_candle = candles[0]
            latest_candle = candles[1]
            prev_volume = float(prev_candle[5])
            current_volume = float(latest_candle[5])
            volume_difference = current_volume / prev_volume
            print(f'symbol:{symbol}|prev:{prev_volume}|cur:{current_volume}|  diff vol={volume_difference}')
            if volume_difference > 1.8 and volume_difference < 3:
                timestamp = int(latest_candle[0]) // 1000
                dt_object = datetime.fromtimestamp(timestamp)
                message = f"Обнаружена разница в объемах {symbol} в {dt_object}: Прошлая: {prev_volume}, Нынешняя: {current_volume}\nразница: {volume_difference}"
                print(f"{chat_id}" + message)
                bot.send_message(chat_id, message)
                break
            prev_volume = current_volume
            await asyncio.sleep(20)
    except asyncio.CancelledError:
        message = f"Мониторинг {symbol} прерван"
        bot.send_message(chat_id, message)
    return