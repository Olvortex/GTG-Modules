# -*- coding: utf-8 -*-
# Module author: @Pharaonis


# Imports
from telethon.tl.functions.channels import CreateChannelRequest
import random, requests, json
from .. import loader


# Module performance
@loader.tds
class TempMailMod(loader.Module):
    """This module allows you to create and manage temporary emailboxes, delay in receiving letters ≈ 10s"""

    strings = {
        "name": "TempEmail"
    }

    # Methods
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


    # Checking and delivering emails to the group
    async def cemailcmd(self, message):
        """Check your current email for new letters"""

        try:

            # Required variables
            group_id = int(self.db.get(owner = str((await self.client.get_me()).id), key = 'emailchat'))
            login = self.db.get(owner = str((await self.client.get_me()).id), key = 'email')
            domain = self.db.get(owner = str((await self.client.get_me()).id), key = 'emaildomain')

            all_letters = requests.get(f'https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}').json()

            letters = int(self.db.get(owner = str((await self.client.get_me()).id), key = 'letters'))

            letters_now = len(all_letters)

            # Void check and duplicate protection
            if str(all_letters) == '[]' or letters_now == letters:
                return await message.delete()

            # Flag indicating the beginning of the receipt of letters
            await message.edit('📬 Receiving..')

            # Receiving the number of letters and sending them
            for i in reversed(range(letters, letters_now)):

                # Getting a unique letter identifier
                letter_id = all_letters[i - letters]['id']

                # Request for letter data
                letter = requests.get(f'https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={letter_id}').json()

                # Sending a letter
                await self.client.send_message(group_id, f'\
📬 Recipient:\n{login}@{domain}\n\n\
👤 Sender:\n{letter["from"]}\n\n\
🎴 Topic: {letter["subject"]}\n\
✏️ Message:\n{letter["textBody"]}')

            # Record the total number of letters received
            self.db.set(owner = str((await self.client.get_me()).id), key = 'letters', value = f'{letters_now}')

            await message.delete()

        except:

            # Creating a group and getting its id
            self.set("group_id", (await self.creategroup()))
            group_id = str(self.get("group_id"))

            # Saving the group ID to which letters will be sent
            self.db.set(owner = str((await self.client.get_me()).id), key = 'emailchat', value = f'-100{group_id}')

            # Explanation
            return await message.edit("⚠️ Chat for receiving emails wasn't found, but a new one was created. Please write the command again")

    
    # Get the current email address from the database
    async def emailcmd(self, message):
        """Get the current email address"""

        login = self.db.get(owner = str((await self.client.get_me()).id), key = 'email')
        domain = self.db.get(owner = str((await self.client.get_me()).id), key = 'emaildomain')

        return await message.edit(f'<pre>{login}@{domain}</pre>')


    # Generate a new emailing address and store it in the database
    async def nemailcmd(self, message):
        """Create a new email address"""

        # Address generation
        symbols = 'abcdefghijklnopqrstuvwxyz1234567890'
        length = random.randint(6, 12)
        login = ''

        for i in range(length):
            login += random.choice(symbols)
        
        domain = random.choice(['wwjmp.com', 'esiix.com'])

        # Saving the address to the database
        self.db.set(owner = str((await self.client.get_me()).id), key = 'email', value = f'{login}')
        self.db.set(owner = str((await self.client.get_me()).id), key = 'emaildomain', value = f'{domain}')

        # Resetting the total number of received letters
        self.db.set(owner = str((await self.client.get_me()).id), key = 'letters', value = 0)

        return await message.edit(f'<pre>{login}@{domain}</pre>')