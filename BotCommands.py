from discord.ext import commands, tasks
import discord.utils
import discord
import locale
import Warnings
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
            member = guilds.get_member(user_id=self.bot.user.id)
            print(member," - ",len(self.bot.guilds))
            await member.edit(nick= new_username)
    
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

    @tasks.loop(seconds=30,reconnect=True)
    async def do_task(self):
        try:
            await self.update_username(str.format('{0:.10f}',self.coin.get_shib_price()))
        except:
            print("Unable to Fetch Shib Price")

    '''
    @tasks.loop(seconds=30,reconnect=True)
    async def unmute_users(self):
        await self.bot.wait_until_ready()

        db = Warnings.DataBaseManagement()
        to_unmute = db.get_to_unmute()
        info = Info.ServerInformation("Data Files/server_info.json")

        guild = self.bot.get_guild(info.server_info["guild_id"])

        muted_role =  guild.get_role(info.server_info["mute_id"])


        for i,row in to_unmute.iterrows():
            user_id = row['user_id']

            member = await guild.fetch_member(user_id)
            print(str(user_id)+" Unmuted")
            await member.remove_roles(muted_role)


        db.delete_muted_users()
    '''
class UpdateGasPrice(CustomBot):
    def __init__(self,bot):
        super().__init__(bot)


    @tasks.loop(seconds=30,reconnect=True)
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
    @tasks.loop(seconds=30,reconnect=True)
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
