import random, requests
from .. import loader, utils

@loader.tds
class TempMailMod(loader.Module):
    """Temporary Email"""

    # strings = {

    # }

    async def nmailcmd(self, message):
        """create a new mail address"""

        symbols = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        login = ''

        while len(login) <= random.randint(5, 11):
            if random.randint(0, 1) == 0:
                login += random.choice(symbols)
            else:
                login += str(random.randint(0, 9))
        
        domain = str(random.choice(["wwjmp.com","esiix.com"]))

        return await message.edit(f'{login}@{domain}')
