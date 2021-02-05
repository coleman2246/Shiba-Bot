from discord.ext import commands, tasks
import discord.utils
import discord
import CoinInfo
import Info



class ChatCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.info = Info.ServerInformation("Data Files/server_info.json")

    @commands.command()
    async def chartex(self,ctx):
        await self.bot.wait_until_ready()
        self.info.update()

        message = self.info.server_info["chartex"]
        await ctx.send(message)

    @commands.command()
    async def twitter(self,ctx):
        await self.bot.wait_until_ready()
        self.info.update()

        message = self.info.server_info["twitter"]
        await ctx.send(message)

    @commands.command()
    async def reddit(self,ctx):
        await self.bot.wait_until_ready()
        self.info.update()

        message = self.info.server_info["reddit"]
        await ctx.send(message)

    @commands.command()
    async def gas(self,ctx):
        await self.bot.wait_until_ready()
        self.info.update()

        try:
            json = CoinInfo.get_eth_gas()
            message = "Fastest: " +str(json["fastest"]/10) + " Fast: "+ str(json["fast"]/10)+ " Average: " + str(json["average"]/10)
        except:
            message = "Cannot get prices from https://ethgasstation.info/"

        await ctx.send(message)
    