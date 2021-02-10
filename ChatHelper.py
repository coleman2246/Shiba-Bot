from discord.ext import commands, tasks
import discord.utils
import discord
import CoinInfo
import Info
import re
import Warnings
import pandas as pd
from discord.utils import get

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
    
    @commands.command()
    async def warn(self,ctx,user,*,reason):
        await self.bot.wait_until_ready()

        author = ctx.message.author

        guild = self.bot.get_guild(self.info.server_info["guild_id"])

        admin_role = guild.get_role(self.info.server_info["admin_id"])
        mod_role = guild.get_role(self.info.server_info["moderator_id"])
    

        if admin_role in author.roles or mod_role in author.roles:
                if user is None:
                    await ctx.send("This Command requires a user to warn")
                    return 
                #<@!114939079384104969>
                try:
                    user_id =  int(re.findall(r'\d+',user)[0])

                    user_obj = self.bot.get_user(user_id)
                except:
                    await ctx.send("Couldn't Find User")
                    return 

                if reason is None:
                    await ctx.send("Please Specifiy a reason for the warning")
                    return 
                

                db = Warnings.DataBaseManagement()

                db.insert_user_warnings(user_id,reason)
            
                df = db.query_user_warnings(user_id)

                warnings = df.shape[0]

                await ctx.send(str(df[["time","reason"]].head(15)))

                await ctx.send(user+ " You Have "+str(warnings)+ " warnings. For every warning you get past 2 messages you get muted for 2^warnings hours" )


                if warnings >= 2:
                    length = 2 ** warnings

                    try:
                        db.insert_user_muted(user_id,mute_length=length)
                    except:
                        await ctx.send("This User is already muted. This warn will count the next time they are warned.")
                        return 

                    await ctx.send(user+" You Have Been muted for "+str(length)+" hours")
                    
                    muted_role =  guild.get_role(self.info.server_info["mute_id"])
                    
                    try:
                        member = await guild.fetch_member(user_id)
                    except:
                        await ctx.send("This user could not be retreived")
                    
                    try:   
                        await member.add_roles(muted_role)
                    except:
                        await ctx.send("This user is already muted")
                    

        else:
            await ctx.send("Only Admins or Mods can use this command")


    @commands.command()
    async def holders(self,ctx):
        await self.bot.wait_until_ready()
        
        
        try:
            json = CoinInfo.get_holders()
            message = "Current Holders: "+str(json)
        except:
            message = "Cannot get holders, likely api limitation by ethplorer.io"

        await ctx.send(message)
