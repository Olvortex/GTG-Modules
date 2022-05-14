# -*- coding: utf-8 -*-
# Module author: @Pharaonis


# Imports
from telethon.tl.functions.channels import CreateChannelRequest
import random, requests, json
from .. import loader, utils


# Module performance
@loader.tds
class TempMailMod(loader.Module):
    """This module allows you to create and manage temporary emailboxes, delay in receiving letters ≈ 10s"""

    strings = {
        "name": "TempEmail"
    }


    def get(self, *args) -> dict:
        return self.db.get(self.strings["name"], *args)

    def set(self, *args) -> None:
        return self.db.set(self.strings["name"], *args)


    # Database configuration
    async def client_ready(self, client, db):
        self.db = db
        self.client = client


    # Create a group for storing emails
    async def creategroup(self):
        return (
            (
                await self.client(
                    CreateChannelRequest(
                        title=f"📮 Geek Email | {(await self.client.get_me()).id}",
                        about="Here you will receive emails using the TempEmail module",
                        megagroup=True,
                    )
                )
            )
            .chats[0].id
        )


    # Generate a new emailing address and store it in the database
    async def nemailcmd(self, message):
        """Create a new email address"""

        symbols = 'abcdefghijklnopqrstuvwxyz1234567890'
        length = random.randint(6, 12)
        login = ''

        for i in range(length):
            login += random.choice(symbols)
        
        domain = random.choice(['wwjmp.com', 'esiix.com'])

        self.db.set(owner = str((await self.client.get_me()).id), key = 'email', value = f'{login}')
        self.db.set(owner = str((await self.client.get_me()).id), key = 'emaildomain', value = f'{domain}')
        self.db.set(owner = str((await self.client.get_me()).id), key = 'letters', value = 0)

        return await message.edit(f'{login}@{domain}')


    # Get the current email address from the database
    async def emailcmd(self, message):
        """Get the current email address"""

        login = self.db.get(owner = str((await self.client.get_me()).id), key = 'email')
        domain = self.db.get(owner = str((await self.client.get_me()).id), key = 'emaildomain')

        return await message.edit(f'{login}@{domain}')
    

    # Checking and delivering emails to the group
    async def cemailcmd(self, message):
        """Check your current email for new letters"""

        # try:

        group_id = int(self.db.get(owner = str((await self.client.get_me()).id), key = 'emailchat'))
        login = self.db.get(owner = str((await self.client.get_me()).id), key = 'email')
        domain = self.db.get(owner = str((await self.client.get_me()).id), key = 'emaildomain')

        all_letters = requests.get(f'https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}').json()

        letters = int(self.db.get(owner = str((await self.client.get_me()).id), key = 'letters'))

        letters_now = len(all_letters)

        if str(all_letters) == '[]' or letters_now - letters == 0:
            return await message.delete()
        
        await message.edit('📬 Received')
        
        for i in reversed(range(letters, letters_now)):

            letter_id = all_letters[i]['id']
            letter = requests.get(f'https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={letter_id}').json()

            await self.client.send_message(group_id, f'\
📬 Recipient:\n{login}@{domain}\n\n\
👤 Sender:\n{letter["from"]}\n\n\
🎴 Topic: {letter["subject"]}\n\
✏️ Message:\n{letter["textBody"]}')
        
        self.db.set(owner = str((await self.client.get_me()).id), key = 'letters', value = f'{letters_now}')
        #await message.delete()

        # except:

        #     self.set("group_id", (await self.creategroup()))
        #     group_id = str(self.get("group_id"))

        #     self.db.set(owner = str((await self.client.get_me()).id), key = 'emailchat', value = f'-100{group_id}')

        #     return await message.edit('⚠️ You deleted the group to receive letters, it was created anew. Write the command again')