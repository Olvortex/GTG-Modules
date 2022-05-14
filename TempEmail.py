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

    # Database configuration
    async def client_ready(self, client, db):
        self.db = db
        self.client = client

    # I create a group to store emailing addresses
    # async def createchat(self):
    #     return (
    #         (
    #             await self.client(
    #                 CreateChannelRequest(
    #                     title=f"📮 Letters | GeekTG",
    #                     about="Here you will receive emails using the TempMail module",
    #                     megagroup=True,
    #                 )
    #             )
    #         )
    #         .chats[0]
    #         .id
    #     )

    # I generate a new mailing address and save it in the group created above
    async def nmailcmd(self, message, db):
        """create a new email address"""

        symbols = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        login = ''

        while len(login) <= random.randint(5, 11):
            if random.randint(0, 1) == 0:
                login += random.choice(symbols)
            else:
                login += str(random.randint(0, 9))
        
        domain = str(random.choice(["wwjmp.com","esiix.com"]))

        db.set(owner = str((await self.client.get_me()).id), key = "email", value = f"{login}@{domain}")
        #return await message.edit(f'Now {login}@{domain}')
        email = db.get(owner = str((await self.client.get_me()).id), key = "email")
        return await message.edit(email)
