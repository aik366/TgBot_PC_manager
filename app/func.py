from aiogram import Bot
from app.database import birthday, birthday_reminder, db_select_id
import requests


async def open_birthday(bot: Bot):
    func_txt = await birthday()
    if func_txt != "none":
        for bot_id in await db_select_id():
            await bot.send_message(bot_id, f'{func_txt}')


async def open_birthday_reminder(bot: Bot):
    func_txt = await birthday_reminder()
    if func_txt != "none":
        for bot_id in await db_select_id():
            await bot.send_message(bot_id, f'{func_txt}')


async def currency():
    data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    bitcoin = requests.get('https://api.coinbase.com/v2/exchange-rates?currency=BTC').json()
    eth = requests.get('https://api.coinbase.com/v2/exchange-rates?currency=ETH').json()

    usd = data['Valute']['USD']['Value']
    eur = data['Valute']['EUR']['Value']
    amd = data['Valute']['AMD']['Value']

    bitcoin = bitcoin['data']['rates']['USD']
    eth = eth['data']['rates']['USD']

    return f'''
1 руб. = {usd:.2f} доллар
1 руб. = {eur:.2f} евро
1000 руб. = {100 / amd * 1000:.0f} драм

BITCOIN - {bitcoin}
ETH - {eth}
            '''


if __name__ == '__main__':
    pass
