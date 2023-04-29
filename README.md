# bin_gachi_bot
Bot to monitor some values on binance

### Installation:
1. git clone git@github.com:Lackronik/bin_gachi_bot.git
2. python -m venv botenv
3. source botenv/bin/activate
4. pip install -r requirements.txt
5. add new file api.json:

{
"bot_token" : "< bot token >",
"binance_api_key" : "< api key >",
"binannce_api_secret" : "< api secret >"
}

6. python main.py