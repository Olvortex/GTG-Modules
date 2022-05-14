# -*- coding: utf-8 -*-
# Module author: @Pharaonis
# Thank you for your help @lil_wonka

# Imports
from telethon.tl.functions.channels import CreateChannelRequest
import random, requests
from .. import loader, utils

# Module performance
@loader.tds
class TempMailMod(loader.Module):
    """This module allows you to create and manage temporary emailboxes, delay in receiving letters ≈ 10s"""

    strings = {
        "name": "TempEmail"
    }
    
    def __init__(self):
        return (
            (
                self.client(
                    CreateChannelRequest(
                        title=f"📮 Geek Letters | {(self.client.get_me()).id}",
                        about="Here you will receive emails using the TempEmail module",
                        megagroup=True,
                    )
                )
            )
            .chats[0]
            .id
        )

    # Database configuration
    async def client_ready(self, client, db):
        self.db = db
        self.client = client
        await createchat

    # I generate a new emailing address and store it in the database
    async def nemailcmd(self, message):
        """create a new email address"""

        symbols = 'abcdefghijklnopqrstuvwxyz1234567890'
        length = random.randint(6, 12)
        login = ''

        for i in range(length):
            login += random.choice(symbols)
        
        domain = random.choice(['wwjmp.com', 'esiix.com'])

        self.db.set(owner = str((await self.client.get_me()).id), key = 'email', value = f'{login}@{domain}')
        return await message.edit(f'{login}@{domain}')

    # I get the current email address from the database
    async def emailcmd(self, message):
        """get the current email address"""

        email = self.db.get(owner = str((await self.client.get_me()).id), key = 'email')
        return await message.edit(email)


