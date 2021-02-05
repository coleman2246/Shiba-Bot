from discord.ext import commands, tasks
import discord.utils
import discord
import CoinInfo
import locale

class UpdatePriceUSD(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @tasks.loop(seconds=30,reconnect=True)
    async def update_username(self):
        await self.bot.wait_until_ready()

        #print(CoinInfo.get_shib_price())
        member = self.bot.guilds[0].get_member(user_id=self.bot.user.id)


        try:
            value = round(CoinInfo.get_shib_price_usd(),10)
            print(str.format('{0:.10f}',value))
            await member.edit(nick= str.format('{0:.10f}',value))
        except:
            print('Error getting price data')



class UpdateGasPrice(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @tasks.loop(seconds=30,reconnect=True)
    async def update_username(self):
        await self.bot.wait_until_ready()

        #print(CoinInfo.get_shib_price())
        member = self.bot.guilds[0].get_member(user_id=self.bot.user.id)

        try:
            json = CoinInfo.get_eth_gas()
            message = str(json["fastest"]/10) + " "+ str(json["fast"]/10)+" " + str(json["average"]/10)
            await member.edit(nick= message)
        except:
            print("Failure getting gas prices")
    
class UpdateVolumeHourly(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @tasks.loop(seconds=30,reconnect=True)
    async def update_username(self):
        await self.bot.wait_until_ready()

        #print(CoinInfo.get_shib_price())
        member = self.bot.guilds[0].get_member(user_id=self.bot.user.id)


        try:
            value = CoinInfo.get_shib_hour_volume_usd()
            print(value)
            await member.edit(nick= f"{value:,}")
        except:
            print('Error getting price data')
