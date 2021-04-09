# bot.py
import os

import discord
from dotenv import load_dotenv

from discord_webhook import DiscordWebhook


def sendMessage():
    webhook = DiscordWebhook(
        url='https://discord.com/api/webhooks/828436507365867520/QmAMxK6lHdVcRo8m8qae1sqODdSM7yMkFLjg5dZ0FRETmNnb4XwPyli_Ok2ADF4MbWOw',
        content='3080 is in stock \n https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440')
    response = webhook.execute()
