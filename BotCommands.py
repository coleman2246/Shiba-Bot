from discord.ext import commands, tasks
import discord.utils
import discord
import locale
import Info
import requests
import CoinInfo


class CustomBot(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.info = Info.ServerInformation("Data Files/server_info.json")
        self.coin = CoinInfo.CoinQuery()

    async def update_username(self,new_username):
        await self.bot.wait_until_ready()
        
        for guilds in self.bot.guilds:
            try:

                member = guilds.get_member(user_id=self.bot.user.id)
                #print(guilds.name)
                await member.edit(nick= new_username)
            except:
                continue

    def get_json(self,enpoint,request_type = "get",params = None):
        r = requests.Session()
        if(request_type == "get"):
            p = r.get(enpoint,json=params)
        else:
            p = r.post(enpoint,json=params)

        return p.json()

class UpdateShibPrice(CustomBot):
    def __init__(self,bot):
        super().__init__(bot)
        self.coin = CoinInfo.TheGraph()

    @tasks.loop(seconds=60,reconnect=True)
    async def do_task(self):
        try:
            price = self.coin.get_shib_price()
            #print(str.format('{0:.10f}',price))
            await self.update_username(str.format('{0:.10f}',price))
        except:
            print("Unable to Fetch Username Shib Price")


class UpdateBonePrice(CustomBot):
    def __init__(self,bot):
        super().__init__(bot)
        self.coin = CoinInfo.TheGraph()

    @tasks.loop(seconds=60,reconnect=True)
    async def do_task(self):
        try:
            price = self.coin.get_bone_price()
            print(str.format('{0:.10f}',price))
            await self.update_username(str.format('{0:.3f}',price))
        except:
            print("Unable to Fetch Username Bone Price")


class UpdateGasPrice(CustomBot):
    def __init__(self,bot):
        super().__init__(bot)


    @tasks.loop(seconds=60,reconnect=True)
    async def do_task(self):
        await self.bot.wait_until_ready()
        
        try:
            await self.update_username(self.coin.get_gas())
        except:
            print("Unable to get Gas Prices") 
        
    
class UpdateVolumeHourly(CustomBot):
    def __init__(self,bot):
        super().__init__(bot)
        self.coin = CoinInfo.TheGraph()

    @tasks.loop(seconds=30,reconnect=True)
    async def do_task(self):
        await self.bot.wait_until_ready()

        try:
            volume = self.coin.get_shib_volume()
            await self.update_username(f"{volume:,}")
        except:
            print('Error getting shib-volume data')

class UpdateShibHolders(CustomBot):
    def __init__(self,bot):
        super().__init__(bot)


    @tasks.loop(seconds=90,reconnect=True)
    async def do_task(self):
        await self.bot.wait_until_ready()
        URL = "https://api.ethplorer.io/getTokenInfo/0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4ce?apiKey=freekey"
                 
        try:
            holders = int(float(self.get_json(URL)["holdersCount"]))
            await self.update_username(f"{holders:,}")
        except:
            print('Error getting shib-holder data')


class UpdateLeashPriceUSD(CustomBot):
    def __init__(self,bot):
        super().__init__(bot)
        self.coin = CoinInfo.TheGraph()
    @tasks.loop(seconds=60,reconnect=True)
    async def do_task(self):
        await self.bot.wait_until_ready()

        try:
            await self.update_username(f"{int(self.coin.get_leash_price()):,}")
        except:
            print('Error getting leash price data')

class UpateLeashHolder(CustomBot):
    def __init__(self,bot):
        super().__init__(bot)

    @tasks.loop(seconds=60,reconnect=True)
    async def do_task(self):
        await self.bot.wait_until_ready()
        URL = "https://api.ethplorer.io/getTokenInfo/0x27c70cd1946795b66be9d954418546998b546634?apiKey=freekey"
                 
        try:
            holders = int(float(self.get_json(URL)["holdersCount"]))
            await self.update_username(f"{holders:,}")
        except:
            print('Error getting leash-holder data')        

class UpdateShibMarketCap(CustomBot):
    def __init__(self,bot):
        super().__init__(bot)
        self.coin = CoinInfo.TheGraph()

    @tasks.loop(seconds=60,reconnect=True)
    async def do_task(self):
        await self.bot.wait_until_ready()
        #print(self.coin.get_shib_marketcap())
        try:
            await self.update_username(f"{int(self.coin.get_shib_marketcap()):,}")
        except:
            print('Error getting leash-holder data')        



class UpdateTotalValueLocked(CustomBot):
    def __init__(self,bot):
        super().__init__(bot)
        self.coin = CoinInfo.TheGraph()

    @tasks.loop(seconds=60,reconnect=True)
    async def do_task(self):
        await self.bot.wait_until_ready()
        #print(self.coin.get_swap_tvl())
        try:
            await self.update_username(f"{int(self.coin.get_swap_tvl()):,}")
        except:
            print('Error getting leash-holder data')        
